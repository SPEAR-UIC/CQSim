import multiprocessing
import random
from exp_theta_two_parts import exp_1 as exp_random
from exp_theta_two_parts import exp_2 as exp_sgst
from exp_polaris_theta import exp_theta as casestudy_siloed_theta
from exp_polaris_theta import exp_polaris as casestudy_siloed_polaris
from exp_polaris_theta import exp_polaris_theta_sgst as casestudy_sgst



if __name__ == "__main__":

    # Set the seed for random
    seed = 100

    lock = multiprocessing.Manager().Lock()

    p = []

    p.append(multiprocessing.Process(target=exp_random, args=(1, 0.5, 1, lock, seed,)))
    p.append(multiprocessing.Process(target=exp_random, args=(1.30, 0.6, 2, lock, seed,)))
    p.append(multiprocessing.Process(target=exp_sgst, args=(1.30, 3, lock, seed,)))
    p.append(multiprocessing.Process(target=exp_sgst, args=(1, 4, lock, seed,)))
    p.append(multiprocessing.Process(target=casestudy_siloed_theta, args=(5, lock, seed,)))
    p.append(multiprocessing.Process(target=casestudy_siloed_polaris, args=(6, lock, seed,)))
    p.append(multiprocessing.Process(target=casestudy_sgst, args=(7, lock, seed,)))

    for proc in p:
        proc.start()
    

    for proc in p:
        proc.join()

    pass