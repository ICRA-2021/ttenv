"""
Generates a set of initial positions of targets and the agent in ttenv.
If you want to have more conditions to generate initial positions other than
the current metadata version, provide values for the additional variables to
the reset function. For example,
    ex_var = {'init_distance_min':10.0,
                'init_distacne_max':15.0,
                'target_direction':False,
                'belief_direction':False,
                'blocked':True }
    obs.reset(**ex_var)
"""
import numpy as np
import envs
import argparse
import pickle
import os, time

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--env', help='environment ID', default='TargetTracking-v1')
parser.add_argument('--render', type=int, default=1)
parser.add_argument('--map', type=str, default="obstacles02")
parser.add_argument('--nb_targets', type=int, default=1)
parser.add_argument('--nb_init_pose', type=int, default=10)
parser.add_argument('--log_dir', type=str, default='.')

args = parser.parse_args()

def main():
    env = envs.make(args.env,
                    'target_tracking',
                    render=bool(args.render),
                    directory=args.log_dir,
                    map_name=args.map,
                    num_targets=args.nb_targets,
                    is_training=False,
                    )
    timelimit_env = env
    while( not hasattr(timelimit_env, '_elapsed_steps')):
        timelimit_env = timelimit_env.env
    init_pose = []
    from logger import TTENV_EVAL_SET
    while(len(init_pose) < args.nb_init_pose): # test episode
        obs, done = env.reset(**TTENV_EVAL_SET[0]), False
        if args.render:
            env.render()
        notes = input("%d, Pass? y/n"%len(init_pose))
        if notes == "y":
            init_pose.append({'agent':timelimit_env.env.agent.state,
                            'targets':[timelimit_env.env.targets[i].state for i in range(args.nb_targets)],
                            'belief_targets':[timelimit_env.env.belief_targets[i].state for i in range(args.nb_targets)]})

    pickle.dump(init_pose, open(os.path.join(args.log_dir,'init_eval_6.pkl'), 'wb'))

if __name__ == "__main__":
    main()
