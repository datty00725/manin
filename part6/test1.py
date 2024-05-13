from manim import *

class ThreeDAxesWithCylinderIntersection(ThreeDScene):
    def construct(self):
        # Set up the 3D axes
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=7,
            y_length=7,
            
            z_length=7
        )
        
        # Create the first cylinder (centered on y-axis)
        cylinder_y = Cylinder(
            radius=1,
            height=5,
            direction=Y_AXIS # Align with y-axis
        )

        # Create the second cylinder (centered on x-axis)
        cylinder_x = Cylinder(
            radius=1,
            height=5,
            direction=X_AXIS # Align with x-axis
        ).set_color(GREEN)  # Set color to green

        # Parameters for intersection calculation
        radius = 1
        height = 5
        resolution = 20  # Increase resolution for more points

        # Function to check if a point is inside both cylinders
        def is_inside_cylinders(x, y, z):
            in_cylinder_y = (x**2 + z**2 <= radius**2) and (abs(y) <= height / 2)
            in_cylinder_x = (y**2 + z**2 <= radius**2) and (abs(x) <= height / 2)
            return in_cylinder_y and in_cylinder_x

        # Generate points and check if they are inside the intersection
        points = []
        for x in np.linspace(-radius, radius, resolution):
            for y in np.linspace(-height/2, height/2, resolution):
                for z in np.linspace(-radius, radius, resolution):
                    if is_inside_cylinders(x, y, z):
                        points.append([x, y, z])

        # Create dots for the intersection points
        intersection_dots = VGroup(*[
            Dot3D(point, color=YELLOW) for point in points
        ])

        # Initial camera orientation
        initial_phi = 75 * DEGREES
        initial_theta = 45 * DEGREES

        # Set initial camera position
        self.set_camera_orientation(phi=initial_phi, theta=initial_theta)

        # Add the axes and the cylinders to the scene
        self.play(FadeIn(axes))
        self.wait(2)
        self.play(FadeIn(cylinder_y))
        self.wait(2)
        self.play(FadeIn(cylinder_x))
        self.wait(2)

        # Remove the original cylinders and add the intersection dots
        self.play(FadeOut(cylinder_y), FadeOut(cylinder_x))
        self.play(FadeIn(intersection_dots))
        self.wait(2)

# To render the scene, run the following in the terminal:
# manim -pql your_script_name.py ThreeDAxesWithCylinderIntersection
