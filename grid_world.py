import warnings

import matplotlib.pyplot as plt
import numpy as np

warnings.filterwarnings("ignore")


##
def gen_grid_world():
    """
    The gen_grid_world function creates a grid world environment.
    The function returns the grid_world and a dictionary that maps each location to an integer or string.
    The dictionary is used for visualization purposes.

    :return: grid_world is a numpy array (9, 10) the grid world and grid_list is a dictionary that can be used
    to convert from numbers to letters
    """
    O = -1e5  # Dangerous places to avoid
    D = 35  # Dirt
    W = -100  # Water
    C = -3000  # Cat
    T = 1000  # Toy
    grid_list = {
        0: "",
        O: "O",
        D: "D",
        W: "W",
        C: "C",
        T: "T",
    }  # this is actually a dictionary
    grid_world = np.array(
        [
            [0, O, O, 0, 0, O, O, 0, 0, 0],  # 1st row of grid (from above to below)
            [0, 0, 0, 0, D, O, 0, 0, D, 0],  # 2nd row of grid (from above to below)
            [0, D, 0, 0, 0, O, 0, 0, O, 0],  # 3rd
            [O, O, O, O, 0, O, 0, O, O, O],  # 4th
            [D, 0, 0, D, 0, O, T, D, 0, 0],  # 5th
            [0, O, D, D, 0, O, W, 0, 0, 0],  # 6th
            [W, O, 0, O, 0, O, D, O, O, 0],  # 7th
            [W, 0, 0, O, D, 0, 0, O, D, 0],  # 8th
            [0, 0, 0, D, C, O, 0, 0, D, 0],
        ]
    )  # 9th
    return grid_world, grid_list


##
def show_world(grid_world, tlt):  # shows grid world without annotations
    """
    The show_world function takes a grid world and its title as arguments.
    It plots the grid world without any annotations, i.e., only the cells themselves are shown,
    and it returns an axis object that can be used to plot additional information on top of this grid.

    :param grid_world: A numpy array (9, 10) the grid world
    :param tlt: string to set the title of the plot
    :return: The plot of the grid world without annotations
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(tlt)
    ax.set_xticks(np.arange(10))  # xticks from 0.5 to 9.5
    ax.set_yticks(np.arange(10))  # yticks from 0.5 to 8.5
    for i in range(10):
        ax.plot([i - 0.5, i - 0.5], [-0.5, 10.5], color="b", linestyle="-", linewidth=1)
        ax.plot([-0.5, 10.5], [i - 0.5, i - 0.5], color="b", linestyle="-", linewidth=1)
    ax.imshow(grid_world, interpolation="nearest", cmap="hot")
    return ax


##
def show_text_state(grid_world, grid_list, ax):  # shows annotations
    """
    The show_text_state function displays the state of each grid cell in a text format.
    The function takes three arguments:
        - grid_world: A numpy array (9, 10) The current states of the world.
        - grid_list: A list containing all possible states and their corresponding integers.
        - ax: The subplot object that is being used to display the GridWorld.

    :param grid_world: Get the shape of the grid
    :param grid_list: a dictionary shows the text of each cell
    :param ax: Draw the annotations on the given axes
    :return: The annotations
    """
    for x in range(grid_world.shape[0]):  # for each row
        for y in range(grid_world.shape[1]):  # for each column
            if grid_world[x, y] >= -3000:  # Dirt, Water, Cat and Toy
                ax.annotate(
                    grid_list[(grid_world[x, y])],
                    xy=(y, x),
                    horizontalalignment="center",
                )


##
def show_policy(policy, ax):
    """
    The show_policy function takes a policy and plots it on the grid.
    It uses the arrow characters to indicate which action is associated with each policy.

    :param policy: A numpy array (9, 10) determines which action to take in each state
    :param ax: Draw the policy on the grid
    :return: A visualization of the policy
    """
    for x in range(policy.shape[0]):
        for y in range(policy.shape[1]):
            if policy[x, y] == 0:
                ax.annotate(r"$\downarrow$", xy=(y, x), horizontalalignment="center")
            elif policy[x, y] == 1:
                ax.annotate(r"$\rightarrow$", xy=(y, x), horizontalalignment="center")
            elif policy[x, y] == 2:
                ax.annotate(r"$\uparrow$", xy=(y, x), horizontalalignment="center")
            elif policy[x, y] == 3:
                ax.annotate(r"$\leftarrow$", xy=(y, x), horizontalalignment="center")
            elif policy[x, y] == 4:
                ax.annotate(r"$\perp$", xy=(y, x), horizontalalignment="center")


# Darstellung 1: koordinate = (1,0)
# Darstellung 2: nummer = 11


def koord_zu_nummer(koordinate):
    return koordinate[0] * 10 + koordinate[1] + 1


def nummer_zu_koord(nummer):
    # 12 zu (1,1)?
    return (int(nummer / 10), (nummer - 1) % 10)


def zelle_in_welt_enthalten(koordinate):
    # x-achse via koordinate 0: Werte von 0 bis 9
    if koordinate[0] < 0 or koordinate[0] > 9:
        return False
    # y-achse via koordinate 1:  Werte von 0 bis 8
    if koordinate[1] < 0 or koordinate[1] > 8:
        return False
    return True


def aktion_als_koord(akt_nummer):
    if akt_nummer == 0:
        return (1, 0)
    if akt_nummer == 1:
        return (0, 1)
    if akt_nummer == 2:
        return (-1, 0)
    if akt_nummer == 3:
        return (0, -1)
    if akt_nummer == 4:
        return (0, 0)


# zelle_in_welt_enthalten((1, 0)) = True
# zelle_in_welt_enthalten((1, -1)) = False


def wahrscheinlichkeiten():
    anzahl_zustände = 90
    anzahl_aktionen = 5

    w_cube = np.zeros((anzahl_zustände, anzahl_aktionen, anzahl_zustände))

    for state_nr in range(anzahl_zustände):
        for action_nr in range(anzahl_aktionen):
            # state von 0 bis 89
            # action von 0 bis 4
            state_koordinate = nummer_zu_koord(state_nr)  # (1,0)
            act_koordinate = aktion_als_koord(action_nr)  # (-1, 0)

            next_state = state_koordinate + act_koordinate

            # 1. Fall: state + action in der Welt enthalten
            # 2. Fall: state + action nicht in der Welt enthalten
            next_state_nr = koord_zu_nummer(next_state)
            w_cube[state_nr, action_nr, next_state_nr] = w


##
def val_iter(R, discount, maxSteps, infHor, probModel=None):
    """
    The val_iter function takes as input the reward matrix R, the discount factor gamma,
    the maximum number of steps maxSteps and a boolean variable infHor that indicates whether
    or not we are using an infinite horizon problem. The function returns two matrices: V and A.
    The first one contains the value function for each state computed through backwards induction.
    The second one contains the optimal actions (0 to 4) for each state. So there are 5 different possible actions.

    :param R: Calculate the value function
    :param discount: Control the importance of future rewards
    :param maxSteps: Define the number of time steps to be considered
    :param infHor: Determine whether the infinite horizon or the finite horizon version of value iteration is used
    :param probModel=None: Pass the transition probability model to the function
    :return: The value function
    """
    # TODO YOUR CODE HERE
    pass


##
def max_action(V, R, discount, probModel=None):
    """
    The max_action function takes in the value function of the next step,
    the reward matrix, and a discount factor. It returns an action-value function
    of current step and an optimal policy for each state. The action-value function
    is calculated by taking the maximum over actions of discounted V(s) + R(s).
    The optimal policy is taken by choosing the action that maximizes this quantity.

    :param V: Compute the q parameter
    :param R: Compute the value function v
    :param discount: Control the importance of future rewards
    :param probModel=None: Pass the transition probability model to the max_action function
    :return: The maximum action-value function
    """
    # TODO YOUR CODE HERE
    pass


##
def find_policy(V, probModel=None):
    """
    The findPolicy function takes in a value function V and outputs the policy matrix.
    The policy matrix is filled with actions that are possible from each state.
    If an action is not possible, then it will be assigned as (0, 0) which means stay.

    :param V: Store the values of each state
    :param probModel=None: Pass the transition model in
    :return: The policy matrix that matches the optimal value function
    """
    # TODO YOUR CODE HERE
    pass


############################

save_figures = True

data = gen_grid_world()
grid_world = data[0]
grid_list = data[1]

# TODO YOUR CODE HERE
prob_model = ...

ax = show_world(grid_world, "Environment")
show_text_state(grid_world, grid_list, ax)
if save_figures:
    plt.savefig("gridworld.pdf")

# TODO Finite Horizon
values = val_iter(...)
values = values[:, :, 0]
show_world(np.maximum(values, 0), "Value Function - Finite Horizon")
if save_figures:
    plt.savefig("value_Fin_15.pdf")

policy = find_policy(...)
ax = show_world(grid_world, "Policy - Finite Horizon")
show_policy(policy, ax)
if save_figures:
    plt.savefig("policy_Fin_15.pdf")

# TODO Infinite Horizon
values = val_iter(...)
show_world(np.maximum(values, 0), "Value Function - Infinite Horizon")
if save_figures:
    plt.savefig("value_Inf_08.pdf")

policy = find_policy(...)
ax = show_world(grid_world, "Policy - Infinite Horizon")
show_policy(policy, ax)
if save_figures:
    plt.savefig("policy_Inf_08.pdf")

# TODO Finite Horizon with Probabilistic Transition
values = val_iter(...)
values = values[:, :, 0]
show_world(
    np.maximum(values, 0),
    "Value Function - Finite Horizon with Probabilistic Transition",
)
if save_figures:
    plt.savefig("value_Fin_15_prob.pdf")

policy = find_policy(...)
ax = show_world(grid_world, "Policy - Finite Horizon with Probabilistic Transition")
show_policy(policy, ax)
if save_figures:
    plt.savefig("policy_Fin_15_prob.pdf")
