import random

import gym
from pogema import GridConfig
import numpy as np
from pogema.animation import AnimationMonitor


class Model:
    def __init__(self, num_agents=1, sizeMap=24, solidity=0.4, seed=1, num_episode_steps=258, obs_radius=3):
        grid_config = GridConfig(num_agents=num_agents,
                                 size=sizeMap,
                                 density=solidity,
                                 seed=seed,
                                 max_episode_steps=num_episode_steps,
                                 obs_radius=obs_radius
                                 )

        self.env = gym.make('Pogema-v0', grid_config=grid_config)
        self.env = AnimationMonitor(self.env)
        self.env.reset()



    def createMatrixOfWeight(self):


        cur_obst = 0
        for i in range(len(self.obs)):
            cur_obst = 0
            for k in range(len(self.obs[0][0])):
                cur_i_visibility_agents = 0
                for p in range(len(self.obs[0][0][k])):
                    #Инвертируем агентов и препятствия
                    if self.obs[i][0][k][p] == 1:
                        self.unitObstacles[i][cur_obst][cur_i_visibility_agents] = 0
                    elif self.obs[i][1][k][p] == 1:
                        self.unitObstacles[i][cur_obst][cur_i_visibility_agents] = 0
                    #Инвертируем свободные поля
                    else:
                        self.unitObstacles[i][cur_obst][cur_i_visibility_agents] = 1

                    if self.obs[i][2][k][p] == 1:
                        self.unitTargets[i][cur_obst][cur_i_visibility_agents] = 1
                    else:
                        self.unitTargets[i][cur_obst][cur_i_visibility_agents] = random.uniform(0.3,0.7)

                    cur_i_visibility_agents += 1
                cur_obst += 1


        temp = 0.4/len(self.unitObstacles[0])
        lst = [ 0 for _ in range(len(self.unitObstacles[0][0])) ]

        for i in range(len(self.unitObstacles[0][0])):
            lst[i] += i * temp


        for l in range(len(lst)-1):
            for i in range(len(self.unitObstacles)):
                for row in range(len(self.unitObstacles[i])):
                    for column in range(len(self.unitObstacles[i][row])):
                        if self.unitObstacles[i][row][column] == lst[l]:
                            if row + 1 < len(self.unitObstacles[i][row]) and self.unitObstacles[i][row + 1][column] not in lst:
                                self.unitObstacles[i][row + 1][column] = lst[l +1]

                            if row - 1 >= 0 and self.unitObstacles[i][row - 1][column] not in lst:
                                self.unitObstacles[i][row - 1][column] = lst[l +1]

                            if column + 1 < len(self.unitObstacles[i][row]) and self.unitObstacles[i][row][column + 1] not in lst:
                                self.unitObstacles[i][row][column + 1] = lst[l +1]

                            if column - 1 >= 0 and self.unitObstacles[i][row][column - 1] not in lst:
                                self.unitObstacles[i][row][column - 1] = lst[l +1]

        temp = 1 / len(self.unitTargets[0])
        lst = [1 for _ in range(len(self.unitTargets[0][0]))]

        for i in range(len(self.unitTargets[0][0])):
            lst[i] -= i * temp


        for l in range(len(lst)-1):
            for i in range(len(self.unitTargets)):
                for row in range(len(self.unitTargets[i])):
                    for column in range(len(self.unitTargets[i][row])):
                        if self.unitTargets[i][row][column] == lst[l]:
                            if row + 1 < len(self.unitTargets[i][row]) and self.unitTargets[i][row + 1][column] not in lst:
                                self.unitTargets[i][row + 1][column] = lst[l + 1]

                            if row - 1 >= 0 and self.unitTargets[i][row - 1][column] not in lst:
                                self.unitTargets[i][row - 1][column] = lst[l + 1]

                            if column + 1 < len(self.unitTargets[i][row]) and self.unitTargets[i][row][column + 1] not in lst:
                                self.unitTargets[i][row][column + 1] = lst[l + 1]

                            if column - 1 >= 0 and self.unitTargets[i][row][column - 1] not in lst:
                                self.unitTargets[i][row][column - 1] = lst[l + 1]


    def multiplication_matrix(self):
        for i in range(len(self.unitObstacles)):
            for j in range(len(self.unitObstacles[i])):
                for k in range(len(self.unitObstacles[i][j])):
                    if self.unitTargets[i][j][k] == 1:
                        self.z[i][j][k] = 1
                    else:
                        self.z[i][j][k] = self.unitObstacles[i][j][k] * self.unitTargets[i][j][k]

    # def test(self):
    #     result = [0 for _ in range(len(self.z))]
    #     nCenter = int(len(self.z[0]) / 2)
    #     self.prev_actions = [0 for _ in range(len(self.z))]
    #
    #     for i in range(len(self.z)):
    #         top = self.z[i][nCenter - 1][nCenter]
    #         left = self.z[i][nCenter][nCenter - 1]
    #         right = self.z[i][nCenter][nCenter + 1]
    #         bottom = self.z[i][nCenter + 1][nCenter]
    #
    #         print()
    #         print(top, left, right, bottom)
    #         print()
    #
    #         a = {
    #             top: "top",
    #             left: "left",
    #             right: "right",
    #             bottom: "bottom"
    #         }
    #
    #         print(max(a))
    #
    #         print(a)
    #         if (a.get(max(a)) == "top"):
    #             if self.prev_actions[i] == 2:
    #                 a.pop(bottom)
    #                 a.pop(top)
    #                 pass
    #             else:
    #                 if obs[i][1][nCenter - 1][nCenter] == 1:
    #                     result[i] = 0
    #                 else:
    #                     result[i] = 1
    #                     self.prev_actions[i] = 1
    #         if (a.get(max(a)) == "right"):
    #             if self.prev_actions[i] == 4:
    #                 a.pop(left)
    #                 a.pop(right)
    #                 if (a.get(max(a)) == "top"):
    #                     if self.prev_actions[i] == 2:
    #                         a.pop(bottom)
    #                         a.pop(top)
    #                         pass
    #                     else:
    #                         if self.obs[i][1][nCenter - 1][nCenter] == 1:
    #                             result[i] = 0
    #                         else:
    #                             result[i] = 1
    #                             self.prev_actions[i] = 1
    #                 pass
    #             else:
    #                 if self.obs[i][1][nCenter][nCenter + 1] == 1:
    #                     result[i] = 0
    #                 else:
    #                     result[i] = 4
    #                     self.prev_actions[i] = 4
    #
    #         print(a)
    #         if (a.get(max(a)) == "left"):
    #             if self.prev_actions[i] == 3:
    #                 a.pop(right)
    #                 a.pop(left)
    #                 if (a.get(max(a)) == "top"):
    #                     if self.prev_actions[i] == 2:
    #                         a.pop(bottom)
    #                         a.pop(top)
    #                         pass
    #                     else:
    #                         if obs[i][1][nCenter - 1][nCenter] == 1:
    #                             result[i] = 0
    #                         else:
    #                             result[i] = 1
    #                             self.prev_actions[i] = 1
    #                 pass
    #             else:
    #                 if obs[i][1][nCenter][nCenter - 1] == 1:
    #                     result[i] = 0
    #                 else:
    #                     result[i] = 3
    #                     self.prev_actions[i] = 3
    #
    #         if (a.get(max(a)) == "bottom"):
    #             if self.prev_actions[i] == 2:
    #                 a.pop(top)
    #                 if (a.get(max(a)) == "top"):
    #                     if self.prev_actions[i] == 2:
    #                         a.pop(bottom)
    #                         pass
    #                     else:
    #                         if obs[i][1][nCenter - 1][nCenter] == 1:
    #                             result[i] = 0
    #                         else:
    #                             result[i] = 1
    #                             self.prev_actions[i] = 1
    #                 pass
    #             print(a)
    #             if (a.get(max(a)) == "left"):
    #                 if self.prev_actions[i] == 3:
    #                     a.pop(right)
    #                     if (a.get(max(a)) == "top"):
    #                         if self.prev_actions[i] == 2:
    #                             a.pop(bottom)
    #                             pass
    #                         else:
    #                             if obs[i][1][nCenter - 1][nCenter] == 1:
    #                                 result[i] = 0
    #                             else:
    #                                 result[i] = 1
    #                                 self.prev_actions[i] = 1
    #                     pass
    #                 else:
    #                     if obs[i][1][nCenter][nCenter - 1] == 1:
    #                         result[i] = 0
    #                     else:
    #                         result[i] = 3
    #                         self.prev_actions[i] = 3
    #             else:
    #                 if obs[i][1][nCenter + 1][nCenter] == 1:
    #                     result[i] = 0
    #                 else:
    #                     result[i] = 2
    #                     self.prev_actions[i] = 2


    def act(self, obs, dones, positions_xy, targets_xy):

        self.obs = obs
        self.agents = positions_xy
        self.targets = targets_xy

        self.unitObstacles = np.array([])
        self.unitObstacles.resize(len(self.agents), len(self.obs[0][0]), len(self.obs[0][0]))

        self.unitTargets = np.array([])
        self.unitTargets.resize(len(self.agents), len(self.obs[0][0]), len(self.obs[0][0]))

        self.z = np.array([])
        self.z.resize(len(self.agents), len(self.unitTargets[0]), len(self.unitTargets[0]))

        self.createMatrixOfWeight()
        self.multiplication_matrix()

        self.prev_act = [0 for _ in range(len(self.z))]

        result = [0 for _ in range(len(self.z))]
        nCenter = int(len(self.z[0]) / 2)

        for i in range(len(self.z)):
            left = self.z[i][nCenter][nCenter - 1]
            right = self.z[i][nCenter][nCenter + 1]
            top = self.z[i][nCenter - 1][nCenter]
            bottom = self.z[i][nCenter + 1][nCenter]

            topIndex = 1
            bottomIndex = 2
            leftIndex = 3
            rightIndex = 4

            a = {
                top: "top",
                left: "left",
                right: "right",
                bottom: "bottom"
            }

            if (a.get(max(a)) == "top"):
                if self.prev_act[i] == topIndex:
                    if obs[i][1][nCenter - 1][nCenter] == 1:
                        self.prev_act[i] = 0
                        result[i] = 0
                    else:
                        self.prev_act[i] = topIndex
                        result[i] = topIndex
                else:
                    self.prev_act[i] = random.randint(0, 4)
                    result[i] = random.randint(0, 4)

            if (a.get(max(a)) == "bottom"):
                if self.prev_act[i] == bottomIndex:
                    if obs[i][1][nCenter - 1][nCenter] == 1:
                        self.prev_act[i] = 0
                        result[i] = 0
                    else:
                        self.prev_act[i] = bottomIndex
                        result[i] = bottomIndex
                else:
                    self.prev_act[i] = random.randint(0, 4)
                    result[i] = random.randint(0, 4)

            if (a.get(max(a)) == "left"):
                if self.prev_act[i] == leftIndex:
                    if obs[i][1][nCenter - 1][nCenter] == 1:
                        self.prev_act[i] = 0
                        result[i] = 0
                    else:
                        self.prev_act[i] = leftIndex
                        result[i] = leftIndex
                else:
                    self.prev_act[i] = random.randint(0, 4)
                    result[i] = random.randint(0, 4)

            if (a.get(max(a)) == "right"):
                if self.prev_act[i] == rightIndex:
                    if obs[i][1][nCenter - 1][nCenter] == 1:
                        self.prev_act[i] = 0
                        result[i] = 0
                    else:
                        self.prev_act[i] = rightIndex
                        result[i] = leftIndex
                else:

                    self.prev_act[i] = random.randint(0,4)
                    result[i] = random.randint(0,4)




        # result = test()
        #
        # for i in range(len(result)):
        #     if result[i] == 1:
        #         for j in range(len(result)):
        #             if result[j] == 1:
        #                 if self.agents[i][1] - 1 == self.agents[j][1] - 1 and self.agents[i][0] == self.agents[j][0]:
        #                     result[i] = 0
        #
        #             elif result[j] == 2:
        #                 if self.agents[i][1] - 1 == self.agents[j][i] + 1 and self.agents[i][0] == self.agents[j][0]:
        #                     result[i] = 0
        #
        #             elif result[i] == 3:
        #                 if self.agents[i][1] - 1 == self.agents[j][i] and self.agents[i][0] == self.agents[j][0] - 1:
        #                     result[i] = 0
        #
        #             elif result[i] == 4:
        #                 if self.agents[i][1] - 1 == self.agents[j][i] and self.agents[i][0] == self.agents[j][0] + 1:
        #                     result[i] = 0
        #
        #     elif result[i] == 2:
        #         for j in range(len(result)):
        #             if result[j] == 1:
        #                 if self.agents[i][1] + 1 == self.agents[j][1] - 1 and self.agents[i][0] == self.agents[j][0]:
        #                     result[i] = 0
        #
        #             elif result[j] == 2:
        #                 if self.agents[i][1] + 1 == self.agents[j][i] + 1 and self.agents[i][0] == self.agents[j][0]:
        #                     result[i] = 0
        #
        #             elif result[i] == 3:
        #                 if self.agents[i][1] + 1 == self.agents[j][i] and self.agents[i][0] == self.agents[j][0] - 1:
        #                     result[i] = 0
        #
        #             elif result[i] == 4:
        #                 if self.agents[i][1] + 1 == self.agents[j][i] and self.agents[i][0] == self.agents[j][0] + 1:
        #                     result[i] = 0
        #
        #     elif result[i] == 3:
        #         for j in range(len(result)):
        #             if result[j] == 1:
        #                 if self.agents[i][1] == self.agents[j][1] - 1 and self.agents[i][0] - 1 == self.agents[j][0]:
        #                     result[i] = 0
        #
        #             elif result[j] == 2:
        #                 if self.agents[i][1] == self.agents[j][i] + 1 and self.agents[i][0] - 1 == self.agents[j][0]:
        #                     result[i] = 0
        #
        #             elif result[i] == 3:
        #                 if self.agents[i][1] == self.agents[j][i] and self.agents[i][0] - 1 == self.agents[j][0] - 1:
        #                     result[i] = 0
        #
        #             elif result[i] == 4:
        #                 if self.agents[i][1] == self.agents[j][i] and self.agents[i][0] - 1 == self.agents[j][0] + 1:
        #                     result[i] = 0
        #
        #     elif result[i] == 4:
        #         for j in range(len(result)):
        #             if result[j] == 1:
        #                 if self.agents[i][1] == self.agents[j][1] - 1 and self.agents[i][0] + 1 == self.agents[j][0]:
        #                     result[i] = 0
        #
        #             elif result[j] == 2:
        #                 if self.agents[i][1] == self.agents[j][i] + 1 and self.agents[i][0] + 1 == self.agents[j][0]:
        #                     result[i] = 0
        #
        #             elif result[i] == 3:
        #                 if self.agents[i][1] == self.agents[j][i] and self.agents[i][0] + 1 == self.agents[j][0] - 1:
        #                     result[i] = 0
        #
        #             elif result[i] == 4:
        #                 if self.agents[i][1] == self.agents[j][i] and self.agents[i][0] + 1 == self.agents[j][0] + 1:
        #                     result[i] = 0

        return result

    def info(self):
        print("Вессы препятствий")
        print(len(self.unitObstacles))
        print("___________________________________")

        print("Весы точек назначений")
        print(len(self.unitTargets))
        print(self.unitTargets)
        print("___________________________________")

        print("Выходные y")
        print(len(self.z))
        print(self.z)
        print("___________________________________")


def main():
    test = Model(num_agents=258, sizeMap=128, solidity=0.3, seed=None)
    obs = test.env.reset()

    done = [False for _ in range(len(obs))]
    while not all(done):
        stemps = test.act(obs, done, test.env.get_agents_xy(), test.env.get_targets_xy())
        obs, reward, done, info = test.env.step(stemps)

    test.env.save_animation("render.svg", egocentric_idx=None)


if __name__ == '__main__':
    main()