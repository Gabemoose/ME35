import requests # you may need to run 'pip install requests' to install this library
import json
from pandas import DataFrame


import rclpy # imports rclpy client library 
from rclpy.node import Node # imports Node class of rclpy library

from geometry_msgs.msg import Twist
from std_msgs.msg import String # imports ROS2 built-in string message type


'''
URL = 'https://api.airtable.com/v0/appMs8xPuIwXYYK6B/Tasks'

#'https://api.airtable.com/v0/' + BaseID + '/' + tableName + '?api_key=' + APIKey

headers = {"Authorization": "Bearer {}".format('keyAMfEmNdROZUlz2')}
r = requests.get(url = URL, headers = headers)
data = r.json()
df = DataFrame(data['records'])
df = df.sort_values(by=['createdTime'])
ind = df.shape[0] - 1

relationships = df.iloc[ind,2]
action = relationships.get("Name")

print(data)
print(df)
print(action)
'''





class air_table(Node):
    
    def __init__(self):
        super().__init__('air_table')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        tick = .1
        
        
        
        self.i = 0
        self.forward = .25
        self.turn = .5
        
        self.url = 'https://api.airtable.com/v0/appMs8xPuIwXYYK6B/Tasks'
        self.key = 'keyAMfEmNdROZUlz2'
        self.timer = self.create_timer(tick, self.timer_callback)
        
    def req (self):
        headers = {"Authorization": "Bearer {}".format(self.key)}
        r = requests.get(url = self.url, headers = headers)
        data = r.json()
        df = DataFrame(data['records'])
        df = df.sort_values(by=['createdTime'])
        ind = df.shape[0] - 1

        relationships = df.iloc[ind,2]
        action = relationships.get("Name")
        return action
    
    def find_motor(self, input):
        if input == 'w':
            x = self.forward
            z = 0
            
            return x, z
        
        elif input == 'a':
            x = 0
            z = self.turn
            
            return x, z
        
        elif input == 'd':
            x = 0
            z = - self.turn
            
            return x, z
        
        elif input == 's':
            x = - self.forward
            z = 0
            
            return x, z
        
        elif input == 'q':
            x = 0
            z = 0
            
            return x, z
        
        else:
            x = 0
            z = 0
            
            return x, z
    
    def timer_callback(self):
        twist = Twist() 

        # Defines string to publish
        input = self.req() #% self.i 
        print(input)
        x, z = self.find_motor(input)

        
        
        twist.linear.x = float(x)
        
        twist.angular.z = float(z)
        
        
        # Publishes `msg` to topic 
        self.publisher_.publish(twist) 

        # Prints `msg.data` to console
        #self.get_logger().info('Publishing: "%s"' % msg.data) 

        # Increments counter
        self.i += 1 

def main(args=None):
    # Initializes ROS2 communication and allows Nodes to be created
    rclpy.init(args=args)
    
        
    # Creates the SimplePublisher Node
    simple_publisher = air_table()

    try:
        # Spins the Node to activate the callbacks
        rclpy.spin(simple_publisher)
        

    # Stops the code if CNTL-C is pressed on the keyboard    
    except KeyboardInterrupt:
        print('\nCaught Keyboard Interrupt')

        # Destroys the node that was created
        simple_publisher.destroy_node()

        # Shuts down rclpy 
        rclpy.shutdown()


if __name__ == '__main__':
    # Runs the main function

    main()