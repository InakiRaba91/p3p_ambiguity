from manim import *

def rotation_matrix(angle, axis):
    if angle == 0:
        return np.eye(3)
    ux, uy, uz = axis
    c, s = np.cos(np.pi*angle/180), np.sin(np.pi*angle/180)
    return  np.array([
        [ux**2 * (1 - c) + c, ux*uy*(1 - c) - uz*s, ux*uz*(1 - c) + uy*s],
        [ux*uy*(1 - c) + uz*s, uy**2 * (1 - c) + c, uy*uz*(1 - c) - ux*s],
        [ux*uz*(1 - c) - uy*s, uy*uz*(1 - c) + ux*s, uz**2 * (1 - c) + c]
    ])

def get_circle_params(p1_3d, p2_3d, p3_3d):
    n = p2_3d - p1_3d
    n = n / np.linalg.norm(n)
    s = (p3_3d - p1_3d).T.dot(n)
    center = p1_3d + s * n
    axis = np.cross(np.array([0, 0, 1]), n)
    axis = axis / np.linalg.norm(axis)
    angle = 180 * np.arccos(n[2]) / np.pi
    radius = np.linalg.norm(p3_3d - center)
    return radius, center, axis, angle

def get_cicle(axes, radius, shift=np.array([0,0,0]), angle=0, axis=np.array([0,0,1]), color=RED):
    circle = ParametricFunction(
        lambda t: axes.c2p(*(np.dot(rotation_matrix(angle, axis), radius * np.array([np.cos(t), np.sin(t), 0])) + shift)),
        color=color,
        t_range=[0, 2 * PI]
    )
    return circle

def get_tetrahedron(o, p1, p2, p3, color, ths):
    th1, th2, th3, th4, th5, th6 = ths
    l1 = Line3D(start=o, end=p1, color=color, thickness=th1)
    l2 = Line3D(start=o, end=p2, color=color, thickness=th2)
    l3 = Line3D(start=o, end=p3, color=color, thickness=th3)
    l4 = Line3D(start=p1, end=p3, color=color, thickness=th4)
    l5 = Line3D(start=p2, end=p3, color=color, thickness=th5)
    l6 = Line3D(start=p1, end=p2, color=color, thickness=th6)
    return l1, l2, l3, l4, l5, l6

class P3PAmbiguity(ThreeDScene):
    def construct(self):
        # Write text with explanation inside a rectangle
        steps = [
            "Setup: three rays $r_1$, $r_2$, $r_3$\\\\with given angles",
            "First solution: $\\{p_1, p_2, p_3\\}$\\\\with known distances",
            "Rotating $p_3$ around $\overline{p_1p_2}$\\\\preserves distances",
            "Second solution: rotate $p_3$\\\\until it lies again in $r_3$",
            "Third solution: move $p_1$\\\\closer and $p_2$ away along their\\\\rays to keep their distance until\\\\the rotated circle intersects with $r_3$",
            "Fourth solution: move $p_2$\\\\closer and $p_1$ away along their\\\\rays to keep their distance until\\\\the rotated circle intersects with $r_3$",
        ]
        texts = [Tex(step, color=WHITE).scale(0.7).to_edge(UP + 0.5 * LEFT) for step in steps]

        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=8,
            y_length=6,
            z_length=6,
        )
        self.add(axes)

        # add xyz labels
        x_label = Text("x").to_edge(5.5*RIGHT+4*DOWN)
        y_label = Text("y").to_edge(7.5*RIGHT+6*UP)
        z_label = Text("z").to_edge(13*RIGHT+0.5*UP)
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label)
        self.add(x_label, y_label, z_label)

        # set camera
        self.set_camera_orientation(phi=70 * DEGREES, theta=-40 * DEGREES, zoom=1.3)

        # draw 
        color_tetrahedron = ORANGE
        color_rays = YELLOW
        color_ct = BLUE_D
        color_circle = RED
        th_l, th_h = 0.005, 0.03
        o_3d = (0, 0, 0)
        p1_3d = np.array([-1, 0, 3])
        p2_3d = np.array([1, 0, 3])
        p3_3d = np.array([0, -np.sqrt(3), 3])
        o, p1, p2, p3 = axes.c2p(*o_3d), axes.c2p(*p1_3d), axes.c2p(*p2_3d), axes.c2p(*p3_3d)
        r1_label = MathTex(r"r_1", color=color_rays).to_edge(12.6*LEFT+0.3*UP)
        r2_label = MathTex(r"r_2", color=color_rays).to_edge(10.4*RIGHT+0.3*UP)
        r3_label = MathTex(r"r_3", color=color_rays).to_edge(10.6*LEFT+0.3*UP)
        p1_label = MathTex(r"p_1", color=color_tetrahedron).to_edge(13.2*LEFT+3*UP)
        p2_label = MathTex(r"p_2", color=color_tetrahedron).to_edge(11.5*RIGHT+4*UP)
        p3_label = MathTex(r"p_3", color=color_tetrahedron).to_edge(11.4*LEFT+5*UP)
        ct_label = MathTex(r"c", color=color_ct).to_edge(13.4*RIGHT+3.5*UP)
        
        r1, r2, r3 = [Line3D(start=o, end=axes.c2p(*10*pt), color=color_rays, thickness=th_l / 2) for pt in [p1_3d, p2_3d, p3_3d]]
        l1, l2, l3, l4, l5, l6 = get_tetrahedron(o=o, p1=p1, p2=p2, p3=p3, color=color_tetrahedron, ths=[th_l] + [th_h]*5)
        radius, center, axis, angle = get_circle_params(p1_3d, p2_3d, p3_3d)
        ct = Dot(axes.c2p(*center), color=color_ct, radius=0.15)
        circle = get_cicle(axes=axes, radius=radius, shift=center, angle=angle, axis=axis, color=color_circle)
        self.add_fixed_in_frame_mobjects(r1_label, r2_label, r3_label, texts[0])
        self.play(*[Create(r) for r in [r1, r2, r3]], *[Write(l) for l in [r1_label, r2_label, r3_label, texts[0]]])
        self.wait(2)
        self.play(FadeOut(texts[0]))
        self.add_fixed_in_frame_mobjects(p1_label, p2_label, p3_label, texts[1])
        self.play(*[Create(l) for l in [l1, l2, l3, l4, l5, l6]], *[Write(l) for l in [p1_label, p2_label, p3_label, texts[1]]])
        self.wait(2)
        self.play(FadeOut(texts[1]))
        self.add_fixed_in_frame_mobjects(ct_label, texts[2])
        self.play(Create(ct), Write(ct_label), Create(circle), Write(texts[2]))
        self.wait(2)

        # second case
        p3_3d = p3_3d / 2
        p3 = axes.c2p(*p3_3d)
        _, _, l3_2, l4_2, l5_2, _ = get_tetrahedron(o=o, p1=p1, p2=p2, p3=p3, color=color_tetrahedron, ths=[th_l] + [th_h]*5)
        self.play(FadeOut(texts[2]))
        self.add_fixed_in_frame_mobjects(texts[3])
        self.play(
            ReplacementTransform(l3, l3_2), 
            ReplacementTransform(l4, l4_2), 
            ReplacementTransform(l5, l5_2),
            p3_label.animate.to_edge(12*LEFT+6.2*UP),
            Write(texts[3]),
        )
        self.wait(2)
        
        # third case
        p1_3d = np.array([-0.72682889, 0, 2.18048668])
        p2_3d = np.array([ 1.03952328, 0, 3.11856984])
        p3_3d = np.array([ 0, -1.69967317, 2.94392029])
        p1, p2, p3 = axes.c2p(*p1_3d), axes.c2p(*p2_3d), axes.c2p(*p3_3d)
        l1_3, l2_3, l3_3, l4_3, l5_3, l6_3 = get_tetrahedron(o=o, p1=p1, p2=p2, p3=p3, color=color_tetrahedron, ths=[th_l, th_h, th_h, th_l, th_h, th_l])
        radius, center, axis, angle = get_circle_params(p1_3d, p2_3d, p3_3d)
        ct_3 = Dot(axes.c2p(*center), color=color_ct, radius=0.15)
        circle_3 = get_cicle(axes=axes, radius=radius, shift=center, angle=angle, axis=axis, color=color_circle)

        self.play(FadeOut(texts[3]))
        self.add_fixed_in_frame_mobjects(texts[4])
        self.play(
            ReplacementTransform(l1, l1_3), 
            ReplacementTransform(l2, l2_3), 
            ReplacementTransform(l3_2, l3_3), 
            ReplacementTransform(l4_2, l4_3), 
            ReplacementTransform(l5_2, l5_3), 
            ReplacementTransform(l6, l6_3),
            ReplacementTransform(circle, circle_3),
            ReplacementTransform(ct, ct_3),
            p1_label.animate.to_edge(13.2*LEFT+3.7*UP),
            p2_label.animate.to_edge(12.2*RIGHT+5*UP),
            p3_label.animate.to_edge(11.2*LEFT+4.8*UP),
            ct_label.animate.to_edge(13.5*RIGHT+3.7*UP),
            Write(texts[4]),
        )
        self.wait(2)

        # fourth case
        p1_3d = np.array([-1.03952328, 0, 3.11856984])
        p2_3d = np.array([ 0.72682889, 0, 2.18048668])
        p1, p2 = axes.c2p(*p1_3d), axes.c2p(*p2_3d)
        l1_4, l2_4, _, l4_4, l5_4, l6_4 = get_tetrahedron(o=o, p1=p1, p2=p2, p3=p3, color=color_tetrahedron, ths=[th_l] + [th_h]*5)
        radius, center, axis, angle = get_circle_params(p1_3d, p2_3d, p3_3d)
        ct_4 = Dot(axes.c2p(*center), color=color_ct, radius=0.15)
        circle_4 = get_cicle(axes=axes, radius=radius, shift=center, angle=angle, axis=axis, color=color_circle)
        self.play(FadeOut(texts[4]))
        self.add_fixed_in_frame_mobjects(texts[5])
        self.play(
            ReplacementTransform(l1_3, l1_4), 
            ReplacementTransform(l2_3, l2_4), 
            ReplacementTransform(l4_3, l4_4), 
            ReplacementTransform(l5_3, l5_4), 
            ReplacementTransform(l6_3, l6_4),
            ReplacementTransform(circle_3, circle_4),
            ReplacementTransform(ct_3, ct_4),
            p1_label.animate.to_edge(13.1*LEFT+2.6*UP),
            p2_label.animate.to_edge(12.1*RIGHT+5.3*UP),
            Write(texts[5]),
        )
        self.wait(2)

# To render the scene, run the following command in your terminal:
# poetry run manim -pql p3p_ambiguity/scenes/p3p_ambiguity.py P3PAmbiguity