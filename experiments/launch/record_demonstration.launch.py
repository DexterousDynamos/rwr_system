from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

# select the cameras to be used

cameras = {"front_view": False, "side_view": True, "wrist_view": False}


def generate_launch_description():
    return LaunchDescription(
        [
            # CAMERA INGRESS NODE
            # Node(
            #     package="ingress",
            #     executable="oakd_node.py",
            #     name="oakd_node",
            #     output="log",
            #     parameters=[
            #         {"enable_front_camera": cameras["front_view"]},
            #         {"enable_side_camera": cameras["side_view"]},
            #         {"enable_wrist_camera": cameras["wrist_view"]},
            #     ],
            # ),
            
            Node(
                package="ingress",
                executable="rokoko_node.py",
                name="rokoko_node",
                output="log",
                parameters=[
                    {"rokoko_tracker/ip": "0.0.0.0"},
                    {"rokoko_tracker/port": 14043},
                    {"rokoko_tracker/use_coil": True}
                ],
            ),

            #  HAND CONTROLLER NODE
            Node(
                package="hand_control",
                executable="hand_control_node.py",
                name="hand_control_node",
                output="screen"
            ),
            
            # RETARGET NODE
            Node(
                package="retargeter",
                executable="retargeter_node.py",
                name="retargeter_node",
                output="screen",
                # COMMENT OR UNCOMMENT THE FOLLOWING LINES TO SWITCH BETWEEN MJCF AND URDF, JUST ONE OF THEM SHOULD BE ACTIVE TODO: Make this a parameter
                parameters=[
                    {
                        "retarget/urdf_filepath": os.path.join(
                            get_package_share_directory("viz"),
                            "models",
                            "orca1_hand",
                            "urdf",
                            "orca1.urdf",
                        ),
                        "retarget/hand_scheme": os.path.join(
                            get_package_share_directory("viz"),
                            "models",
                            "orca1_hand",
                            "scheme_orca1.yaml",
                        ),
                        "retarget/mano_adjustments": os.path.join(
                            get_package_share_directory("experiments"),
                            "cfgs",
                            "retargeter_adjustment.yaml"
                        ),
                        "retarget/retargeter_cfg": os.path.join(
                            get_package_share_directory("experiments"),
                            "cfgs",
                            "retargeter_cfgs_orca1.yaml"
                        ),
                    },
                    {"debug": True},
                    {"include_wrist_and_tower": True},
                ],
            ), 
            
            # VISUALIZATION NODE
            
            # Node(
            #     package="viz",
            #     executable="visualize_joints.py",
            #     name="visualize_joints",
            #     parameters=[
            #         {
            #             "scheme_path": os.path.join(
            #                 get_package_share_directory("viz"),
            #                 "models",
            #                 "orca1_hand",
            #                 "scheme_orca1.yaml",
            #             )
            #         }
            #     ],
            #     output="screen",
            # ),
        ]
    )
