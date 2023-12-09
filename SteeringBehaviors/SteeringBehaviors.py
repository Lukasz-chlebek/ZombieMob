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

    def seek(self, target:pygame.Vector2) -> pygame.Vector2:
        desiredVelocity = (target - self.vehicle.Pos()).normalize() * self.vehicle.maxForce
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

    def calculate(self) -> pygame.Vector2:
        wander = self.wander() * 1
        wall_avoidance = self.wall_avoidance() * 10
        obstacle_avoidance = self.obstacles_avoidance() * 10
        hide = self.hide() * 4
        flee = self.flee(pygame.Vector2(pygame.mouse.get_pos()))
        accumulatedForce = wander + wall_avoidance + obstacle_avoidance + hide + flee
        return accumulatedForce
        return self.obstacles_avoidance()*10 + self.flee(pygame.Vector2(pygame.mouse.get_pos())) + self.wander()
        return self.flee(pygame.Vector2(pygame.mouse.get_pos()))
        return self.wander()
                                            
def randomClamped() -> float:
    return random.random() * 2 - 1