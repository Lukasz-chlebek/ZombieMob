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
        self.wanderJitter:float = 30
        self.wanderTarget = pygame.Vector2(0,0)


    def seek(self, target:pygame.Vector2) -> pygame.Vector2:
        desiredVelocity = (target - self.vehicle.Pos()).normalize() * self.vehicle.maxForce
        return desiredVelocity - self.vehicle.velocity


    def flee(self, target:pygame.Vector2) -> pygame.Vector2:      
        if target.distance_squared_to(self.vehicle.Pos()) > self.panicDistanceSq:
            return pygame.Vector2(0,0)
        
        desiredVelocity = (self.vehicle.Pos() - target).normalize() * self.vehicle.maxForce
        return desiredVelocity - self.vehicle.velocity
    

    def wander(self) -> pygame.Vector2:
        self.wanderTarget += pygame.Vector2(randomClamped() * self.wanderJitter, randomClamped() * self.wanderJitter)
        self.wanderTarget = self.wanderTarget.normalize()
        self.wanderTarget *= self.wanderRadius
        targetLocal = self.wanderTarget + pygame.Vector2(self.wanderDistance, 0)
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
            closest_intersect_obstacle.color = (255, 0, 0)
            return pygame.Vector2(steeringForceX,steeringForceY).rotate(-heading_angle)
        else:
            return pygame.Vector2(0,0)

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
        return self.seek(best_hiding_spot) # zmienic na arrive

    def calculate(self) -> pygame.Vector2:
        return self.hide() + self.flee(pygame.Vector2(pygame.mouse.get_pos())) + 5* self.wander()
        return self.obstacles_avoidance()*10 + self.flee(pygame.Vector2(pygame.mouse.get_pos())) + self.wander()
        return self.flee(pygame.Vector2(pygame.mouse.get_pos()))
        return self.wander()
                                            
def randomClamped() -> float:
    return random.random() * 2 - 1