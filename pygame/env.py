# env.py
import math
from MyGame import Map, WORLD_WIDTH, WORLD_HEIGHT

ACTIONS = {
    0: (0, -1),  # up
    1: (0, 1),  # down
    2: (-1, 0),  # left
    3: (1, 0),  # right
}


class SimpleGridEnv:
    """
    Entorno mínimo para NEAT:
    - Observación: [player_x_norm, player_y_norm, goal_x_norm, goal_y_norm,
                    dx_norm, dy_norm, dist_norm]
    - Acciones: 0=up,1=down,2=left,3=right
    - Recompensa: shaping por distancia + bonus al llegar
    """

    def __init__(self, width=WORLD_WIDTH, height=WORLD_HEIGHT, max_steps=200):
        self.width = width
        self.height = height
        self.max_steps = max_steps
        self.map = Map(width, height)
        self.steps = 0
        self._last_dist = None

    def _pos(self):
        px, py = self.map.player.get_position(self.map)
        gx, gy = self.map.goal.get_position(self.map)
        return px, py, gx, gy

    def _dist(self, px, py, gx, gy):
        # Distancia Manhattan; puedes probar euclídea si prefieres
        return abs(px - gx) + abs(py - gy)

    def reset(self):
        # Recoloca jugador y meta como hace tu Map.__init__
        self.map = Map(self.width, self.height)
        self.steps = 0
        px, py, gx, gy = self._pos()
        self._last_dist = self._dist(px, py, gx, gy)
        return self._obs()

    def _obs(self):
        px, py, gx, gy = self._pos()
        # Normalizaciones a [0,1]
        pxn = px / (self.width - 1)
        pyn = py / (self.height - 1)
        gxn = gx / (self.width - 1)
        gyn = gy / (self.height - 1)
        dx = gx - px
        dy = gy - py
        dxn = dx / (self.width - 1)
        dyn = dy / (self.height - 1)
        dist = self._dist(px, py, gx, gy)
        distn = dist / (self.width + self.height - 2)  # máx Manhattan
        return [pxn, pyn, gxn, gyn, dxn, dyn, distn]

    def step(self, action: int):
        self.steps += 1
        move = ACTIONS.get(action, (0, 0))
        px, py, gx, gy = self._pos()
        nx, ny = px + move[0], py + move[1]

        # Intenta mover (tu Map ya ignora fuera de límites)
        if self.map.is_inside(nx, ny):
            self.map.move_player(nx, ny)

        # Recompensa: mejora de distancia
        px2, py2, gx2, gy2 = self._pos()
        dist = self._dist(px2, py2, gx2, gy2)
        reward = (self._last_dist - dist) * 0.5  # shaping suave
        self._last_dist = dist

        done = False
        win = (px2, py2) == (gx2, gy2)
        if win:
            reward += 5.0  # bonus por llegar
            done = True

        # penalización leve por paso para evitar bucles
        reward -= 0.01

        if self.steps >= self.max_steps:
            done = True

        return self._obs(), reward, done, {"win": win}
