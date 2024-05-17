from manim import *


class FourierCirclesSceneWithCamera(ZoomedScene):
    def __init__(self, 
    n_vectors=10,
    big_radius=2,
    vector_config={
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
    },
    circle_color=BLUE,
    circle_config={
            "stroke_width": 1,
        },
    base_frequency=1,
    slow_factor=0.5,
    Hide_0th_vector=True,
    parametric_function_step_size=0.001,
    drawn_path_color=WHITE,
    drawn_path_stroke_width=2,
    interpolate_config=[0,1],
    zoomed_display_height= 3,
    zoomed_display_width= 4,
    image_frame_stroke_width=3,
    zoom_factor=0.3,
    default_frame_stroke_width=0.1,
    cairo_line_width_multiple=0.01,
    zoom_camera_to_full_screen_config= {
            "run_time": 3,
            "func": smooth,
            "velocity_factor": 1
        },
    zoomed_display_corner=UL,
    zoomed_display_corner_buff=0.0,
    **kwargs,
    ):
        self.circle_color=circle_color
        self.n_vectors=n_vectors
        self.big_radius=big_radius
        self.vector_config=vector_config
        self.circle_config=circle_config
        self.base_frequency=base_frequency
        self.slow_factor=slow_factor
        self.parametric_function_step_size=parametric_function_step_size
        self.drawn_path_color=drawn_path_color
        self.drawn_path_stroke_width=drawn_path_stroke_width
        self.interpolate_config=interpolate_config
        self.zoomed_display_height=zoomed_display_height
        self.zoomed_display_width=zoomed_display_width
        self.image_frame_stroke_width=image_frame_stroke_width
        self.zoom_factor=zoom_factor
        self.default_frame_stroke_width=default_frame_stroke_width
        self.cairo_line_width_multiple=cairo_line_width_multiple
        self.zoom_camera_to_full_screen_config=zoom_camera_to_full_screen_config
        
        self.Hide_0th_vector=Hide_0th_vector
        self.zoomed_display_corner=zoomed_display_corner
        self.zoomed_display_corner_buff=zoomed_display_corner_buff
        self.zoom_position=lambda mob: mob.next_to(self.zoomed_display_corner,buff=self.zoomed_display_corner_buff) 
        ZoomedScene.__init__(self,camera_class=MultiCamera, zoom_factor=self.zoom_factor,zoomed_display_width=self.zoomed_display_width,
        zoomed_display_height=self.zoomed_display_height,
        image_frame_stroke_width=self.image_frame_stroke_width,
        zoomed_display_corner=self.zoomed_display_corner,
        zoomed_display_corner_buff=self.zoomed_display_corner_buff,
        **kwargs)
        self.slow_factor_tracker = ValueTracker(
            self.slow_factor
        )
        def add_dt(m,dt):
            m.increment_value(dt*self.slow_factor_tracker.get_value())
        self.vector_clock = ValueTracker(0.0).add_updater(add_dt)
        self.add(self.vector_clock)

    

    def setup(self):
        ZoomedScene.setup(self)
        

    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()

    def get_vector_time(self):
        return self.vector_clock.get_value()

    def get_freqs(self):
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))
        all_freqs.sort(key=abs)
        return all_freqs

    def get_coefficients(self):
        return [complex(0) for _ in range(self.n_vectors)]

    def get_color_iterator(self):
        return itertools.cycle(self.drawn_path_color)

    def get_rotating_vectors(self, freqs=None, coefficients=None):
        vectors = VGroup()
        self.center_tracker = VectorizedPoint(ORIGIN)

        if freqs is None:
            freqs = self.get_freqs()
        if coefficients is None:
            coefficients = self.get_coefficients()

        last_vector = None
        
        for i in range(len(freqs)):
            freq=freqs[i]
            coefficient=coefficients[i]
            if last_vector:
                center_func = last_vector.get_end
            else:
                center_func = self.center_tracker.get_location
            if i<len(freqs)-1:
                vector = self.get_rotating_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func,
            )
            else:
                vector=self.get_rotating_last_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func,
            )
            if (i==0 and self.Hide_0th_vector):
                vector.set_opacity(0)
            vectors.add(vector)
            last_vector = vector
        return vectors



    def get_rotating_vector(self, coefficient, freq, center_func):
        vector = Vector(abs(coefficient)*RIGHT, **self.vector_config)
        #vector.scale(abs(coefficient))
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        vector.add_updater(self.update_vector)
        return vector

    def update_vector(self, vector, dt):
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag

        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        return vector

    def update_last_vector(self, vector, dt):
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag

        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        #vector_end=vector.get_end()
        #self.zoomed_camera.frame.move_to(vector_end)
        return vector

    def get_rotating_last_vector(self, coefficient, freq, center_func):
        vector = Vector(abs(coefficient)*RIGHT, **self.vector_config)
        #vector.scale(abs(coefficient))
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        vector.add_updater(self.update_last_vector)
        return vector

    def get_circles(self, vectors):
        ans=VGroup(*[
            self.get_circle(
                vector,
            )
            for vector in vectors
        ])
        if self.Hide_0th_vector:
            ans[0].set_opacity(0)
        return ans

    def get_circle(self, vector):
        circle = Circle(color=self.circle_color, **self.circle_config)
        circle.center_func = vector.get_start
        circle.radius_func = vector.get_length
        circle.add_updater(self.update_circle)
        return circle

    def update_circle(self, circle):
        circle.set(width=2 * circle.radius_func())
        circle.move_to(circle.center_func())
        return circle

    def get_vector_sum_path(self, vectors, color=YELLOW):
        coefs = np.array([v.coefficient for v in vectors])
        freqs = np.array([v.freq for v in vectors])
        center = vectors[0].get_start()
        def compute_curve(t):
            return complex_to_R3(coefs.dot(np.exp(TAU*1j*freqs*t)))
        """lambda t: center + functools.reduce(operator.add, [
                complex_to_R3(
                    coef * np.exp(TAU * 1j * freq * t)
                )
                for coef, freq in zip(coefs, freqs)
            ])"""

        path = ParametricFunction(compute_curve
            ,
            t_range=[0,1,self.parametric_function_step_size],
            color=self.drawn_path_color,use_smoothing=False
        )
        return path

    def get_drawn_path_alpha(self):
        return self.get_vector_time()

    def get_drawn_path(self, vectors, stroke_width=None, fade=False, **kwargs):
        if stroke_width is None:
            stroke_width = self.drawn_path_stroke_width
        path = self.get_vector_sum_path(vectors, **kwargs)
        broken_path = CurvesAsSubmobjects(path)
        broken_path.curr_time = 0
        start, end = self.interpolate_config

        def update_path(path, dt):
            alpha = self.get_drawn_path_alpha()
            n_curves = len(path)
            for a, sp in zip(np.linspace(0, 1, n_curves), path):
                b = (alpha - a)
                if b < 0:
                    width = 0
                else:
                    if fade:
                        width = stroke_width * interpolate(start, end, (1 - (b % 1)))
                    else:
                        width = stroke_width
                sp.set_stroke(width=width)
            path.curr_time += dt
            return path

        broken_path.set_color(self.drawn_path_color)
        broken_path.add_updater(update_path)
        return broken_path



    def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        samples -= ORIGIN
        complex_samples = samples[:, 0] + 1j * samples[:, 1]

        return [
            np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt for freq in freqs
        ]

    #Setup the vector clock 
    

    def zoom_config(self):
        self.activate_zooming(animate=False)
        self.zoomed_display.to_corner(self.zoomed_display_corner,buff=self.zoomed_display_corner_buff)
        #self.zoom_position(self.zoomed_display)
        self.zoomed_camera.frame.add_updater(lambda mob: mob.move_to(self.vectors[-1].get_end()))
        self.zoomed_camera.cairo_line_width_multiple =self.cairo_line_width_multiple
        self.zoomed_camera.default_frame_stroke_width=self.default_frame_stroke_width

    

    def scale_zoom_camera_to_full_screen_config(self):
        BigSquare=Rectangle(height=self.camera.frame_height,width=self.camera.frame_width).shift(self.camera.frame_width*self.zoomed_display_corner[0]*RIGHT).shift(self.camera.frame_height*self.zoomed_display_corner[1]*UP)

        # This is not in the original version of the code.
        def fix_update(mob, dt, velocity_factor, dt_calculate):
            if dt == 0 and mob.counter == 0:
                rate = velocity_factor * dt_calculate
                mob.counter += 1
            else:
                rate = dt * velocity_factor
            if dt > 0:
                mob.counter = 0
            return rate
        
        fps = 1 / self.camera.frame_rate
        mob = self.zoomed_display
        mob.counter = 0
        velocity_factor = self.zoom_camera_to_full_screen_config["velocity_factor"]
        mob.start_time = 0
        run_time = self.zoom_camera_to_full_screen_config["run_time"]
        run_time *= 2
        mob_height=mob.height
        mob_width=mob.width
        #mob_height = mob.get_height()
        #mob_width = mob.get_width()
        mob_center = mob.get_center()
        ctx = self.zoomed_camera.cairo_line_width_multiple
        frame_width=self.default_frame_stroke_width
 
        def update_camera(mob, dt):
            mob.start_time += fix_update(mob, dt, velocity_factor, fps)
            if mob.start_time <= run_time:
                alpha = mob.start_time / run_time
                alpha_func = self.zoom_camera_to_full_screen_config["func"](alpha)
                mob.stretch_to_fit_height(
                    interpolate(
                        mob_height,
                        self.camera.frame_height,#The default camera height is 4
                        alpha_func
                    )
                )
                mob.stretch_to_fit_width(interpolate(mob_width,self.camera.frame_width,alpha_func))

                self.zoomed_camera.cairo_line_width_multiple = interpolate(
                    ctx,
                    self.camera.cairo_line_width_multiple*.3,
                    alpha_func
                )
                self.zoomed_camera.frame.set_stroke(width=interpolate(frame_width,
                        0,
                        alpha_func)
                    )
                mob.next_to(BigSquare,-self.zoomed_display_corner,buff=self.zoomed_display_corner_buff)
            return mob

        self.zoomed_display.add_updater(update_camera)

# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
 
#   ____          _                  
#  / ___|   _ ___| |_ ___  _ __ ___  
# | |  | | | / __| __/ _ \| '_ ` _ \ 
# | |__| |_| \__ \ || (_) | | | | | |
#  \____\__,_|___/\__\___/|_| |_| |_|
 
#     _          _                 _   _                 
#    / \   _ __ (_)_ __ ___   __ _| |_(_) ___  _ __  ___ 
#   / _ \ | '_ \| | '_ ` _ \ / _` | __| |/ _ \| '_ \/ __|
#  / ___ \| | | | | | | | | | (_| | |_| | (_) | | | \__ \
# /_/   \_\_| |_|_|_| |_| |_|\__,_|\__|_|\___/|_| |_|___/
# x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
 


class Normal(FourierCirclesSceneWithCamera):
    def construct(self):
        super().__init__(n_vectors=200,#控制向量数量
        slow_factor=1/10,#控制时间长短，slow factor越小，画的速度越慢,      
        cairo_line_width_multiple=0.01,#控制缩放镜头里线的长短
        default_frame_stroke_width=0.1,)#控制缩放镜头边框长短
        f=open(r"music.txt","r")
        freqs=[]
        coefs=[]
        lines=f.readlines()
        for line in lines:
            a,b=line.split()
            freqs.append(int(a))
            coefs.append(complex(b))

        coefs=coefs[:self.n_vectors]
        freqs=freqs[:self.n_vectors]
        coefs=np.array(coefs)
        freqs=np.array(freqs)
        #coefs[0]控制了图像的中心位置，需要微调到最适合的位置。
        coefs/=110
        coefs[0]=-0.5j

        music_vector=self.get_rotating_vectors(coefficients=coefs,freqs=freqs)
        music_circle=self.get_circles(music_vector)
        music_drawn_path=self.get_drawn_path(music_vector)

        self.add(music_vector,music_circle,music_drawn_path)
        self.vectors=music_vector#Need to define vectors for zoom_config to work
        self.wait(1/self.slow_factor)

class ZoomToFullScreen(FourierCirclesSceneWithCamera):
    def construct(self):
        super().__init__(n_vectors=200,#控制向量数量
        slow_factor=1/30,#控制时间长短，slow factor越小，画的速度越慢,      
        cairo_line_width_multiple=0.01,#控制缩放镜头里线的长短
        default_frame_stroke_width=0.1,
        zoomed_display_corner=UR,
        zoomed_display_corner_buff=0,
        zoom_camera_to_full_screen_config= {
            "run_time": 5,
            "func": there_and_back_with_pause,
            "velocity_factor": 1
        })#控制缩放镜头边框长短
        f=open(r"music.txt","r")
        freqs=[]
        coefs=[]
        lines=f.readlines()
        for line in lines:
            a,b=line.split()
            freqs.append(int(a))
            coefs.append(complex(b))

        coefs=coefs[:self.n_vectors]
        freqs=freqs[:self.n_vectors]
        coefs=np.array(coefs)
        freqs=np.array(freqs)
        #coefs[0]控制了图像的中心位置，需要微调到最适合的位置。
        coefs/=110
        coefs[0]=-0.5j

        music_vector=self.get_rotating_vectors(coefficients=coefs,freqs=freqs)
        music_circle=self.get_circles(music_vector)
        music_drawn_path=self.get_drawn_path(music_vector)

        self.add(music_vector,music_circle,music_drawn_path)
        #下面两行开启左上的缩放镜头，若不需要可删除
        self.vectors=music_vector#Need to define vectors for zoom_config to work
        self.zoom_config()
        self.wait(10)
        self.scale_zoom_camera_to_full_screen_config()
        self.wait(20)