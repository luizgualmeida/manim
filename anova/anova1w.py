from manim import *
from scipy.stats import f
import numpy as np

class ANOVAAnimation(Scene):
    def construct(self):
        # Ajustes de posicionamento
        LEFT_SECTION = LEFT * 2.5  # Movendo tudo para a esquerda
        RIGHT_SECTION = RIGHT * 4  # Movendo tudo mais para a direita

        # Criando o círculo grande que engloba os grupos
        big_circle = Circle(radius=3.2, color=WHITE).shift(LEFT_SECTION)

        # Criando os três grupos com círculos inicialmente maiores
        initial_group_radius = 1.2 
        final_group_radius = 0.35  
        group1 = Circle(radius=initial_group_radius, color=BLUE).shift(LEFT_SECTION + LEFT * 1)
        group2 = Circle(radius=initial_group_radius, color=GREEN).shift(LEFT_SECTION + RIGHT * 1)
        group3 = Circle(radius=initial_group_radius, color=RED).shift(LEFT_SECTION + UP * 0.3)

        # Criando rótulos para os grupos
        label1 = Text("Grupo 1", color=BLUE).scale(0.5).next_to(group1, DOWN)
        label2 = Text("Grupo 2", color=GREEN).scale(0.5).next_to(group2, DOWN)
        label3 = Text("Grupo 3", color=RED).scale(0.5).next_to(group3, UP)

        # Função para gerar pontos dentro de um círculo específico
        def generate_points(center, radius, color, spread_factor=0.2):
            points = VGroup()
            for _ in range(10):
                while True:
                    x = np.random.uniform(-radius, radius)
                    y = np.random.uniform(-radius, radius)
                    point = np.array([x, y, 0]) + center
                    if np.linalg.norm(point - center) <= radius:
                        break
                points.add(Dot(point=point, color=color))
            return points

        # Gerando pontos dentro dos grupos
        points_group1 = generate_points(group1.get_center(), initial_group_radius, BLUE)
        points_group2 = generate_points(group2.get_center(), initial_group_radius, GREEN)
        points_group3 = generate_points(group3.get_center(), initial_group_radius, RED)

        # Criando a média geral (ponto branco)
        global_mean = Dot(color=WHITE).scale(1.2).shift(LEFT_SECTION)

        # Criando as médias dos grupos
        group1_mean = Dot(color=PURE_BLUE).scale(1.0).move_to(group1.get_center())
        group2_mean = Dot(color=PURE_GREEN).scale(1.0).move_to(group2.get_center())
        group3_mean = Dot(color=PURE_RED).scale(1.0).move_to(group3.get_center())

        # Fórmula do F de Fisher
        formula_F = MathTex("F = \\frac{\\text{Variância entre grupos}}{\\text{Variância dentro dos grupos}}"
        ).scale(0.7).to_edge(UP).shift(RIGHT_SECTION)  # Movido mais para a direita


        formula_F[0][2:23].set_color(ORANGE)
        formula_F[0][24:34].set_color(BLUE)
        formula_F[0][34:40].set_color(GREEN)
        formula_F[0][40:50].set_color(RED)


        # Criando eixo X e Y para o gráfico da distribuição F
        f_distribution = Axes(
            x_range=[0, 6, 1],  # Eixo x com valores inteiros
            y_range=[0, 1, 0.2],
            axis_config={"color": WHITE}
        ).scale(0.7).shift(RIGHT_SECTION + RIGHT * 1.5 + DOWN * 1.2)  # Movido mais para a direita

        v = w = 5
        f_curve = f_distribution.plot(lambda x: f.pdf(x, v, w), color=YELLOW)

        # Adicionando ponto no gráfico para o primeiro momento (x < 2)
        point_initial = Dot(f_distribution.c2p(1.5, f.pdf(1.5, v, w)), color=WHITE, radius=0.07)

        # Adicionando ponto no gráfico para o segundo momento (x = 4)
        point_final = Dot(f_distribution.c2p(4, f.pdf(4, v, w)), color=WHITE, radius=0.07)

        # Criando setas sólidas entre a média geral e as médias dos grupos
        arrow_global_to_g1 = always_redraw(lambda: Arrow(global_mean.get_center(), group1_mean.get_center(), color=ORANGE))
        arrow_global_to_g2 = always_redraw(lambda: Arrow(global_mean.get_center(), group2_mean.get_center(), color=ORANGE))
        arrow_global_to_g3 = always_redraw(lambda: Arrow(global_mean.get_center(), group3_mean.get_center(), color=ORANGE))

        # Criando setas tracejadas das médias dos grupos para um ponto dentro do grupo
        arrow_g1_to_point = always_redraw(lambda: DashedLine(group1_mean.get_center(), points_group1[0].get_center(), color=BLUE))
        arrow_g2_to_point = always_redraw(lambda: DashedLine(group2_mean.get_center(), points_group2[0].get_center(), color=GREEN))
        arrow_g3_to_point = always_redraw(lambda: DashedLine(group3_mean.get_center(), points_group3[0].get_center(), color=RED))

        # Adicionando elementos à cena
        self.play(Create(big_circle))
        self.play(Create(global_mean), Create(points_group1), Create(points_group2), Create(points_group3))
        self.wait(2)

        self.play(Create(group1), Create(group2), Create(group3))
        self.play(Write(label1), Write(label2), Write(label3))
        self.play(Create(group1_mean), Create(group2_mean), Create(group3_mean))
        self.wait(2)

        
        # Criando as setas sólidas entre a média geral e as médias dos grupos
        self.add(arrow_global_to_g1, arrow_global_to_g2, arrow_global_to_g3)
        self.wait(1)

        # Criando as setas tracejadas das médias dos grupos para um ponto dentro de cada grupo
        self.play(Create(arrow_g1_to_point), Create(arrow_g2_to_point), Create(arrow_g3_to_point))
        self.wait(2)

        # Adicionando elementos do lado direito

        # Fórmula
        self.play(Write(formula_F))
        self.wait()

        # Adicionando o gráfico à cena
        self.play(Create(f_distribution), Create(f_curve), Create(point_initial))
        self.wait(2)

        # Transição para os grupos se afastando e reduzindo o tamanho
        self.play(
            group1.animate.shift(LEFT * 1).scale(0.5),  
            group2.animate.shift(RIGHT * 1).scale(0.5),
            group3.animate.shift(UP * 1).scale(0.5),
            points_group1.animate.shift(LEFT * 0.1),
            points_group2.animate.shift(RIGHT * 0.1),
            points_group3.animate.shift(UP * 0.1),
            group1_mean.animate.shift(LEFT * 1),
            group2_mean.animate.shift(RIGHT * 1),
            group3_mean.animate.shift(UP * 1),
            label1.animate.shift(UL * 0.6 + LEFT * 0.4),
            label2.animate.shift(UR * 0.6 + RIGHT * 0.4),
            label3.animate.shift(UP * 0.5),
        )
        

         # No segundo momento, centralizar os pontos dentro dos círculos menores
        centered_points_group1 = generate_points(group1.get_center() + LEFT * 0.1, final_group_radius, BLUE, spread_factor=0.1)
        centered_points_group2 = generate_points(group2.get_center() + RIGHT * 0.1, final_group_radius, GREEN, spread_factor=0.1)
        centered_points_group3 = generate_points(group3.get_center() + UP * 0.1, final_group_radius, RED, spread_factor=2)

        self.play(
            Transform(points_group1, centered_points_group1),
            Transform(points_group2, centered_points_group2),
            Transform(points_group3, centered_points_group3),
        )

        # Atualizando fórmula do F para valores significativos
        # Transição para o segundo ponto na curva (x = 4)
        self.play(Transform(point_initial, point_final))
        
        self.wait(2)
