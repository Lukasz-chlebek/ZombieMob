import pygame
import random
import math
import globals
import line


class SteeringBehaviors:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.panicDistance:float = 100
        self.panicDistanceSq:float = self.panicDistance ** 2
        self.wanderRadius:float = 100
        self.wanderDistance:float = 30
        self.wanderJitter:float = 10
        self.wanderTarget = pygame.Vector2(0,0)
        self.wall_distance_avoid = self.vehicle.radius * 10
        self.wander_weights = {
            "wander": 3,
            "wall_avoidance": 10 if self.vehicle.is_in_world else 0,
            "obstacles_avoidance": 10,
            "hide": 7,
            "flee_from_mouse": 0,
            "flee_from_player": 2,
            "separation": 2.5,
            "seek": 0.1,
            "alignment": 2,
            "cohesion": 2
        }
        self.attack_weights = {
            "wander": 2,
            "wall_avoidance": 10 if self.vehicle.is_in_world else 0,
            "obstacles_avoidance": 10,
            "hide": 0,
            "flee_from_mouse": 1,
            "flee_from_player": 0,
            "separation": 20,
            "seek": 1,
            "alignment": 10,
            "cohesion": 10
        }

        self.weights = self.wander_weights
        self.attack_distance = 125
        self.attack_distance_sq = self.attack_distance ** 2
        self.number_of_neighbors_to_attack = 20

    def seek(self, target:pygame.Vector2) -> pygame.Vector2:
        temp = (target - self.vehicle.Pos())
        if temp.length() != 0:
            desiredVelocity = temp.normalize() * self.vehicle.maxForce
        else:
            desiredVelocity = pygame.Vector2(0,0)
        return desiredVelocity - self.vehicle.velocity

    def arrive(self, target:pygame.Vector2):
        to_target = target- self.vehicle.position
        dist = to_target.length()
        if dist > 0:
            deceleration_tweaker = 0.3
            speed = dist/(deceleration_tweaker * 2)
            speed = min(speed, self.vehicle.maxVelocity)
            desired_velocity = to_target * speed /dist
            return desired_velocity - self.vehicle.velocity
        return pygame.Vector2(0,0)

    def flee(self, target:pygame.Vector2) -> pygame.Vector2:      
        if target.distance_squared_to(self.vehicle.Pos()) > self.panicDistanceSq:
            return pygame.Vector2(0,0)
        
        desiredVelocity = (self.vehicle.Pos() - target).normalize() * self.vehicle.maxForce
        return desiredVelocity - self.vehicle.velocity
    

    def wander(self) -> pygame.Vector2:
        #self.wanderTarget.rotate_ip(-self.vehicle.velocity.angle_to(self.wanderTarget))
        #globals.lines.append(line.Line(self.vehicle.position, self.vehicle.position + self.wanderTarget))
        self.wanderTarget += pygame.Vector2(randomClamped() * self.wanderJitter, randomClamped() * self.wanderJitter)
        self.wanderTarget = self.wanderTarget.normalize()
        self.wanderTarget *= self.wanderRadius
        targetLocal = self.wanderTarget + pygame.Vector2(self.wanderDistance, 0)
        globals.lines.append(line.Line(self.vehicle.position, self.vehicle.position + targetLocal))
        return targetLocal

    def obstacles_avoidance(self):
        min_detection_box = 50
        box_Length = min_detection_box + (self.vehicle.velocity.length() / self.vehicle.maxVelocity) * min_detection_box
        dist_to_closest_ip = 9999999
        local_pos_of_closest_obstacle = pygame.Vector2()
        closest_intersect_obstacle = None

        heading_angle = self.vehicle.velocity.angle_to(pygame.Vector2(1, 0))
        globals.lines.append(line.Line(self.vehicle.position, self.vehicle.position + pygame.Vector2(box_Length,0).rotate(-heading_angle), (255,0,0)))
        for obstacle in globals.OBSTACLES:
            obstacle.color = (120, 255, 120)
            #otagowane tylko
            local_pos:pygame.Vector2 = (obstacle.position - self.vehicle.position).rotate(heading_angle)
            if local_pos.x >= 0 and local_pos.length() - obstacle.radius <= box_Length:
                globals.lines.append(line.Line(self.vehicle.position, pygame.Vector2(self.vehicle.position + local_pos.rotate(-heading_angle))))
                expanded_radius = obstacle.radius + self.vehicle.radius
                if math.fabs(local_pos.y) < expanded_radius:
                    cX = local_pos.x
                    cY = local_pos.y
                    sqrt_part = math.sqrt(expanded_radius*expanded_radius-cY*cY)
                    ip = cX - sqrt_part
                    if ip <= 0:
                        ip = cX + sqrt_part
                    if ip < dist_to_closest_ip:
                        dist_to_closest_ip = ip
                        closest_intersect_obstacle = obstacle
                        local_pos_of_closest_obstacle = local_pos

        if closest_intersect_obstacle is not None:
            multiplier = 1.0 + (box_Length - local_pos_of_closest_obstacle.x) / box_Length
            steeringForceY = (closest_intersect_obstacle.radius - local_pos_of_closest_obstacle.y )*multiplier
            brakingWeight = 0.1
            steeringForceX = (closest_intersect_obstacle.radius - local_pos_of_closest_obstacle.x) * brakingWeight
            globals.lines.append(line.Line(self.vehicle.position, pygame.Vector2(self.vehicle.position + local_pos_of_closest_obstacle.rotate(-heading_angle)),  (0,0,255)))
            return pygame.Vector2(steeringForceX,steeringForceY).rotate(-heading_angle)
        else:
            return pygame.Vector2(0,0)

    def create_feelers(self):
        feelers = []
        heading = self.vehicle.heading
        feelers.append(self.vehicle.position + self.wall_distance_avoid * heading)
        feelers.append(self.vehicle.position + self.wall_distance_avoid/2.0 * heading.rotate(90))
        feelers.append(self.vehicle.position + self.wall_distance_avoid/2.0 * heading.rotate(-90))
        return feelers
     
    def line_intersection_2D(self, A:pygame.Vector2, B:pygame.Vector2, C:pygame.Vector2, D:pygame.Vector2):
        rTop = (A.y-C.y)*(D.x-C.x)-(A.x-C.x)*(D.y-C.y)
        rBot = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)

        sTop = (A.y-C.y)*(B.x-A.x)-(A.x-C.x)*(B.y-A.y)
        sBot = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)
        dist = 0
        point:pygame.Vector2 = pygame.Vector2(0,0)
        if ( (rBot == 0) or (sBot == 0)):
            return (False, dist, point)
        
        r = rTop/rBot
        s = sTop/sBot

        if( (r > 0) and (r < 1) and (s > 0) and (s < 1) ):
            dist = A.distance_to(B) * r
            point = A + r * (B - A)
            return (True, dist, point)

        else:   
            dist = 0
        return (False, dist, point)
    

    def wall_avoidance(self):
        feelers = self.create_feelers()
  
        DistToThisIP    = 0.0
        DistToClosestIP = 10000000.0

        ClosestWall = -1

        SteeringForce = pygame.Vector2() 
        point = pygame.Vector2()         
        ClosestPoint = pygame.Vector2() 
        walls = [
            {"from": pygame.Vector2(0, 0), "to": pygame.Vector2(0, globals.HEIGHT), "normal": pygame.Vector2(1,0)},
            {"from": pygame.Vector2(globals.WIDTH,0), "to": pygame.Vector2(globals.WIDTH, globals.HEIGHT), "normal": pygame.Vector2(-1,0)},
            {"from": pygame.Vector2(0,0), "to": pygame.Vector2(globals.WIDTH, 0), "normal": pygame.Vector2(0,1)},
            {"from": pygame.Vector2(0, globals.HEIGHT), "to": pygame.Vector2(globals.WIDTH, globals.HEIGHT), "normal": pygame.Vector2(0,-1)}
        ]

        for flr, feeler in enumerate(feelers):
            globals.lines.append(line.Line(self.vehicle.position, feeler))
            for w, wall in enumerate(walls):
                intersect, DistToThisIP, point = self.line_intersection_2D(self.vehicle.position, feeler, wall["from"], wall["to"])
                if (intersect == True):
                    if (DistToThisIP < DistToClosestIP):        
                        DistToClosestIP = DistToThisIP
                        ClosestWall = w
                        ClosestPoint = point
            
            if (ClosestWall >= 0):
                #calculate by what distance the projected position of the agent
                #will overshoot the wall
                OverShoot:pygame.Vector2 = feeler - ClosestPoint
                #create a force in the direction of the wall normal, with a 
                #magnitude of the overshoot
                SteeringForce = walls[ClosestWall]["normal"] * OverShoot.length()
        globals.lines.append(line.Line(self.vehicle.position, self.vehicle.position + SteeringForce, (255,0,0)))
        return SteeringForce
    

    def get_hiding_position(self, obstacles_pos: pygame.Vector2, obstacle_radius: float, target_pos: pygame.Vector2):
        distance_from_boundary = 30
        dist_away = obstacle_radius + distance_from_boundary
        to_obstacle = (obstacles_pos - target_pos).normalize()
        return (to_obstacle * dist_away) + obstacles_pos

    def hide(self):
        dist_to_closest = 9999999
        best_hiding_spot = pygame.Vector2
        closest = None
        for obstacle in globals.OBSTACLES:
            hiding_spot = self.get_hiding_position(obstacle.position, obstacle.radius, globals.PLAYER.position)
            ySeparation = hiding_spot.y - self.vehicle.position.y
            xSeparation = hiding_spot.x - self.vehicle.position.x
            dist = ySeparation*ySeparation + xSeparation*xSeparation
            if dist < dist_to_closest:
                dist_to_closest = dist
                best_hiding_spot = hiding_spot
                closest = obstacle
        if dist_to_closest == 9999999:
            return pygame.Vector2(0,0) #tu evade
        return self.arrive(best_hiding_spot) # zmienic na arrive


    def separation(self): 
        SteeringForce:pygame.Vector2 = pygame.Vector2(0,0)
        neighbors = self.vehicle.neighbors
        for a, neighbor in enumerate(neighbors):
            #make sure this agent isn't included in the calculations and that
            #the agent being examined is close enough. ***also make sure it doesn't
            #include the evade target ***
            if(neighbors[a] != self.vehicle):     
                ToAgent:pygame.Vector2 = self.vehicle.position - neighbors[a].position

                #//scale the force inversely proportional to the agents distance  
                #//from its neighbor.
                if ToAgent.length() != 0:
                    SteeringForce += (ToAgent).normalize()/ToAgent.length()
            
        return SteeringForce

    """
    //---------------------------- Alignment ---------------------------------
    //
    //  returns a force that attempts to align this agents heading with that
    //  of its neighbors
    //------------------------------------------------------------------------
    """
    def alignment(self):
    
        #used to record the average heading of the neighbors
        AverageHeading:pygame.Vector2 = pygame.Vector2(0,0)

        #//used to count the number of vehicles in the neighborhood
        NeighborCount = len(self.vehicle.neighbors)

        #iterate through all the tagged vehicles and sum their heading vectors
        neighbors = self.vehicle.neighbors
        for a, neighbor in enumerate(neighbors):  
            #make sure *this* agent isn't included in the calculations and that
            #the agent being examined  is close enough ***also make sure it doesn't
            #include any evade target ***
            if(neighbor != self.vehicle):
                AverageHeading += neighbor.heading 
            
        #if the neighborhood contained one or more vehicles, average their
        #heading vectors.
        if (NeighborCount > 0):
            AverageHeading /= NeighborCount
            AverageHeading -= self.vehicle.heading
    
        return AverageHeading
    
    """
    //-------------------------------- Cohesion ------------------------------
    //
    //  returns a steering force that attempts to move the agent towards the
    //  center of mass of the agents in its immediate area
    //------------------------------------------------------------------------
    """
    def cohesion(self):
        
        #first find the center of mass of all the agents
        CenterOfMass:pygame.Vector2 = pygame.Vector2(0,0)
        SteeringForce:pygame.Vector2 = pygame.Vector2(0,0)

        NeighborCount = len(self.vehicle.neighbors)

        #iterate through the neighbors and sum up all the position vectors
        for a, neighbor in enumerate(self.vehicle.neighbors): 
            #make sure *this* agent isn't included in the calculations and that
            #the agent being examined is close enough ***also make sure it doesn't
            #include the evade target ***
            if(self.vehicle != neighbor):
                CenterOfMass += neighbor.position

        if (NeighborCount > 0):
            #the center of mass is the average of the sum of positions
            CenterOfMass /= NeighborCount
            #now seek towards that position
            SteeringForce = self.seek(CenterOfMass)

        #the magnitude of cohesion is usually much larger than separation or
        #allignment so it usually helps to normalize it.
        if SteeringForce.length() != 0:
            return SteeringForce.normalize()
        else:
            return SteeringForce


    def check_if_attack(self, deltaTime):
        #chance to attack within 5s based on number of neigbhors
        chance = min(len(self.vehicle.neighbors) / self.number_of_neighbors_to_attack, 1) * deltaTime / 5
        print("1", chance)
        #chance to attack within 0.5s based on distance to player
        chance += min(self.attack_distance_sq / self.vehicle.position.distance_squared_to(globals.PLAYER.position), 1) * deltaTime / 2
        print("2", chance)
        if random.random() <= chance:
            self.vehicle.attack()


    def calculate(self, deltaTime) -> pygame.Vector2:
        if not self.vehicle.is_attacking:
            self.check_if_attack(deltaTime)
        wander = self.wander() * self.weights["wander"]
        wall_avoidance = self.wall_avoidance() * self.weights["wall_avoidance"] if self.vehicle.is_in_world else pygame.Vector2(0,0)
        obstacle_avoidance = self.obstacles_avoidance() * self.weights["obstacles_avoidance"]
        hide = self.hide() * self.weights["hide"]
        flee_from_mouse = self.flee(pygame.Vector2(pygame.mouse.get_pos())) * self.weights["flee_from_mouse"]
        flee_from_player = self.flee(globals.PLAYER.position) * self.weights["flee_from_player"]
        separation = self.separation() * self.weights["separation"]
        seek = self.seek(globals.PLAYER.position) * self.weights["seek"]
        cohesion = self.cohesion() * self.weights["cohesion"]
        alignment = self.alignment() * self.weights["alignment"]
        accumulatedForce: pygame.Vector2 = wander + wall_avoidance + obstacle_avoidance + hide + flee_from_mouse + flee_from_player + separation + seek + cohesion + alignment

        return accumulatedForce
        return self.obstacles_avoidance()*10 + self.flee(pygame.Vector2(pygame.mouse.get_pos())) + self.wander()
        return self.flee(pygame.Vector2(pygame.mouse.get_pos()))
        return self.wander()
                                            
def randomClamped() -> float:
    return random.random() * 2 - 1