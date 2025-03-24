from manim import *


class ChangeOfCoordinates(ThreeDScene):
    def construct(self):
        # Write text with explanation inside a rectangle
        steps = [
            "Two different coordinates systems",
            "Three points with known\\\\distances and angles",
            "Build vectors $\overrightarrow{p_1p_2}$ and $\overrightarrow{p_1p_3}$",
            "Vectors can be expressed in both systems",
            "Goal: find rigid transform to\\\\map world vectors to camera vectors",
            "Shift both sets of vectors to origin",
            "Rotate world vectors to align $\overrightarrow{p_1p_2}$",
            "Rotate world vectors to align $\overrightarrow{p_1p_3}$",
            "Shift back to original position",
        ]
        texts = [Tex(step, color=WHITE).scale(0.7).to_edge(3*DOWN + 0.5 * LEFT) for step in steps]

        axes_world = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=8,
            y_length=6,
            z_length=6,
        )
        self.add(axes_world)

        # camera system, another set of 3d axes rotated and shifted
        axes_cam = ThreeDAxes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            z_range=[-1.5, 1.5, 1],
            x_length=2,
            y_length=1.5,
            z_length=1.5,
            x_axis_config={"color": PINK},
            y_axis_config={"color": PINK},
            z_axis_config={"color": PINK},
        )
        ct = 4*DOWN+4*LEFT+2*OUT
        s = np.array([2/3, 1/2, 1/2])
        angle_x, angle_y = 3*PI/8, -PI/4
        axes_cam.rotate(angle_x, RIGHT).rotate(angle_y, UP)
        axes_cam.shift(np.multiply(ct, s))
        self.add(axes_cam)

        # set camera
        self.set_camera_orientation(phi=70 * DEGREES, theta=-40 * DEGREES, zoom=1.3)

        world_label = Tex("World\\\\system", color=WHITE).scale(0.7).to_edge(11.5*RIGHT+0.5*UP)
        cam_label = Tex("Camera\\\\system", color=PINK).scale(0.7).to_edge(5*LEFT+1.5*UP)
        self.add_fixed_in_frame_mobjects(world_label, cam_label)
        self.play(Write(world_label), Write(cam_label))

        # points 
        R = rotation_matrix(angle=angle_y, axis=UP).dot(rotation_matrix(angle=angle_x, axis=RIGHT))
        p1_3d_cam = np.array([-1, 0, 3])
        p2_3d_cam = np.array([1, 0, 3])
        p3_3d_cam = np.array([0, -np.sqrt(3), 3])
        p1_cam, p2_cam, p3_cam = axes_world.c2p(*p1_3d_cam), axes_world.c2p(*p2_3d_cam), axes_world.c2p(*p3_3d_cam)
        dot1_cam, dot2_cam, dot3_cam = [Dot(p, color=ORANGE) for p in [p1_cam, p2_cam, p3_cam]]
        v1_cam, v2_cam = Vector(direction=p2_cam-p1_cam, color=GREEN_E).shift(p1_cam), Vector(direction=p3_cam-p1_cam, color=GREEN_E).shift(p1_cam)
        pts_3d_cam = np.concatenate([p1_3d_cam[:, None], p2_3d_cam[:, None], p3_3d_cam[:, None]], axis=1)

        pts_3d_world = np.dot(R, pts_3d_cam) + ct[:, None]
        p1_3d_world, p2_3d_world, p3_3d_world = pts_3d_world.T
        p1_world, p2_world, p3_world = axes_world.c2p(*p1_3d_world), axes_world.c2p(*p2_3d_world), axes_world.c2p(*p3_3d_world)
        dot1_world, dot2_world, dot3_world = [Dot(p, color=BLUE) for p in [p1_world, p2_world, p3_world]]
        v1_world = Vector(direction=p2_world-p1_world, color=RED).shift(p1_world)
        v2_world = Vector(direction=p3_world-p1_world, color=RED).shift(p1_world)

        self.add_fixed_in_frame_mobjects(texts[0])
        self.play(Write(texts[0]))
        self.wait(2)
        self.play(FadeOut(texts[0]))
        self.add_fixed_in_frame_mobjects(texts[1])
        self.play(FadeOut(world_label),FadeOut(cam_label), Create(dot1_world), Create(dot2_world), Create(dot3_world), Write(texts[1]))
        self.wait(2)
        self.play(FadeOut(texts[1]))
        self.add_fixed_in_frame_mobjects(texts[2])
        self.play(Create(v1_world), Create(v2_world), Write(texts[2]))
        self.wait(2)
        
        # [I|p1I] [R|0] [I|-p1W] = [I|p1I] [R|-R*p1W] = [R|-R*p1W+p1I]
        # [R'.T|-R'.T*T]
        # 1. R'=R.T
        # 2. R'.T*T = R*p1W-R*R.T*p1I = R*(p1W-R.T*p1I)
        # 3. T = p1W-R.T*p1I
        dot1_world_copy, dot2_world_copy, dot3_world_copy = dot1_world.copy(), dot2_world.copy(), dot3_world.copy()
        v1_world_copy, v2_world_copy = v1_world.copy(), v2_world.copy()
        self.play(FadeOut(texts[2]))
        self.add_fixed_in_frame_mobjects(texts[3])
        self.play(
            ReplacementTransform(axes_cam, axes_world), 
            Transform(dot1_world_copy, dot1_cam),
            Transform(dot2_world_copy, dot2_cam),
            Transform(dot3_world_copy, dot3_cam),
            Transform(v1_world_copy, v1_cam),
            Transform(v2_world_copy, v2_cam),
            Write(texts[3])
        )
        self.wait(2)

        self.play(FadeOut(texts[3]))
        self.add_fixed_in_frame_mobjects(texts[4])
        self.play(Write(texts[4]))
        self.wait(2)

        # shift to origin
        pts_3d_cam_orig = pts_3d_cam - p1_3d_cam[:, None]
        pts_3d_world_orig = pts_3d_world - p1_3d_world[:, None]
        p2_3d_world_orig, p3_3d_world_orig = pts_3d_world_orig.T[1:]
        v1_cam_orig, v2_cam_orig = v1_cam.copy(), v2_cam.copy()
        self.play(FadeOut(texts[4]))
        self.add_fixed_in_frame_mobjects(texts[5])
        self.play(
            FadeOut(dot1_world, dot2_world, dot3_world),
            VGroup(v1_cam_orig, v2_cam_orig).animate.shift(-p1_cam).set_color(GREEN_A),
            VGroup(v1_world, v2_world).animate.shift(-p1_world),
            Write(texts[5])
        )
        self.wait(2)

        # rotate to fit v1
        p2_3d_cam_orig, p3_3d_cam_orig = pts_3d_cam_orig.T[1:]
        angle1 = np.arccos(np.dot(p2_3d_cam_orig, p2_3d_world_orig) / (np.linalg.norm(p2_3d_cam_orig) * np.linalg.norm(p2_3d_world_orig)))
        axis1 = np.cross(p2_3d_cam_orig, p2_3d_world_orig)
        axis1 = axis1 / np.linalg.norm(axis1)
        R1 = rotation_matrix(angle=-angle1, axis=axis1)
        pts_3d_world_rot1 = np.dot(R1, pts_3d_world_orig)
        p2_3d_world_rot1, p3_3d_world_rot1 = pts_3d_world_rot1.T[1:]
        p2_world_rot1, p3_world_rot1 = axes_world.c2p(*p2_3d_world_rot1), axes_world.c2p(*p3_3d_world_rot1)
        v1_world_rot1 = Vector(direction=p2_world_rot1, color=RED)
        v2_world_rot1 = Vector(direction=p3_world_rot1, color=RED)
        self.play(FadeOut(texts[5]))
        self.add_fixed_in_frame_mobjects(texts[6])
        self.play(ReplacementTransform(v1_world, v1_world_rot1), ReplacementTransform(v2_world, v2_world_rot1), Write(texts[6]))
        self.wait(2)

        # rotate to fit v2
        angle2 = np.arccos(np.dot(p3_3d_cam_orig, p3_3d_world_rot1) / (np.linalg.norm(p3_3d_cam_orig) * np.linalg.norm(p3_3d_world_rot1)))
        axis2 = np.cross(p3_3d_cam_orig, p3_3d_world_rot1)
        axis2 = axis2 / np.linalg.norm(axis2)
        R2 = rotation_matrix(angle=-angle2, axis=axis2)
        pts_3d_world_rot2 = np.dot(R2, pts_3d_world_rot1)
        p3_3d_world_rot2 = pts_3d_world_rot2.T[-1]
        p3_world_rot2 = axes_world.c2p(*p3_3d_world_rot2)
        v2_world_rot2 = Vector(direction=p3_world_rot2, color=RED)
        self.play(FadeOut(texts[6]))
        self.add_fixed_in_frame_mobjects(texts[7])
        self.play(ReplacementTransform(v2_world_rot1, v2_world_rot2), Write(texts[7]))
        self.wait(2)

        # shift back to original position
        self.play(FadeOut(texts[7]))
        self.add_fixed_in_frame_mobjects(texts[8])
        self.play(
            FadeOut(v1_cam_orig, v2_cam_orig),
            VGroup(v1_world_rot1, v2_world_rot2).animate.shift(p1_cam),
            Write(texts[8])
        )
        self.wait(2)


        

# To render the scene, run the following command in your terminal:
# poetry run manimgl gram_schmidt_3d_span_3d.py GramSchmidt3DSpan3D