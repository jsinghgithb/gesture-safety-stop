import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from cv_bridge import CvBridge
import mediapipe as mp
import cv2


class GestureDetector(Node):
    def __init__(self):
        super().__init__('gesture_detector')
        self.subscription = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10)
        self.publisher_ = self.create_publisher(Bool, 'gesture_event', 10)
        self.bridge = CvBridge()

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, max_num_hands=1, min_detection_confidence=0.6)

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        stop_detected = False
        status_text = "No hand detected"
        status_color = (0, 0, 255)  # red

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw the hand skeleton on the frame so you can SEE what MediaPipe sees
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                extended_count = self.count_extended_fingers(hand_landmarks)
                status_text = f"Hand detected - {extended_count}/4 fingers extended"

                if extended_count >= 3:
                    stop_detected = True
                    status_text += "  -> OPEN PALM (STOP)"
                    status_color = (0, 255, 0)  # green
                else:
                    status_color = (0, 165, 255)  # orange

        # Overlay status text on the frame
        cv2.putText(frame, status_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

        # Show the live window
        cv2.imshow('Gesture Detector - Debug View', frame)
        cv2.waitKey(1)

        out_msg = Bool()
        out_msg.data = stop_detected
        self.publisher_.publish(out_msg)

        if stop_detected:
            self.get_logger().info('STOP gesture detected')

    def count_extended_fingers(self, landmarks):
        tips = [8, 12, 16, 20]
        knuckles = [6, 10, 14, 18]
        extended_count = 0
        for tip, knuckle in zip(tips, knuckles):
            if landmarks.landmark[tip].y < landmarks.landmark[knuckle].y:
                extended_count += 1
        return extended_count


def main(args=None):
    rclpy.init(args=args)
    node = GestureDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()