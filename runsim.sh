#!/usr/bin/env bash

rm -r results
mkdir results

NUM_PROCS=32

# ALPHA - Message rate (milliseconds)
ALPHA=500

# DELTA - Message delay (milliseconds)
DELTA=200

INTERVAL=10

EPSILON=30

# Function to calculate the number of bits required to store an integer
num_bits() {
    number=$1
    bits=0
    while ((number > 0)); do
        ((bits++))
        number=$((number >> 1))
    done
    echo $bits
}



today=$(date +"%Y-%m-%d")


for (( EPSILON=1000; EPSILON>=100; EPSILON-=100)); do
    for (( INTERVAL=$EPSILON; INTERVAL>=$EPSILON; INTERVAL-=10)); do
        if (( INTERVAL * EPSILON % 1000 == 0 && INTERVAL*EPSILON <= 10000 )); then
            for (( DELTA=1; DELTA<=16; DELTA*=2)); do
                for (( ALPHA=20; ALPHA<=160; ALPHA*=2)); do
                    for (( NUM_PROCS=2; NUM_PROCS<=64; NUM_PROCS+=2)); do
                        MAX_OFFSET_SIZE=$(num_bits $EPSILON)

                        echo "N.${NUM_PROCS}-E.${EPSILON}-I.${INTERVAL}-D.${DELTA}-A.${ALPHA}-M.${MAX_OFFSET_SIZE}"    

                        touch replay-config.h

                        echo "#define REPCL_CONFIG_H" >> replay-config.h

                        echo "#define NUM_PROCS $NUM_PROCS" >> replay-config.h

                        echo "#define EPSILON $EPSILON" >> replay-config.h
                        echo "#define INTERVAL $INTERVAL" >> replay-config.h
                        echo "#define ALPHA $ALPHA" >> replay-config.h
                        echo "#define DELTA $DELTA" >> replay-config.h

                        echo "#define MAX_OFFSET_SIZE $MAX_OFFSET_SIZE" >> replay-config.h

                        rm src/replay-config.h
                        mv replay-config.h src/

                        make

                        bin/comparison | tee -a results/results-${today}-N.${NUM_PROCS}-E.${EPSILON}-I.${INTERVAL}-D.${DELTA}-A.${ALPHA}-M.${MAX_OFFSET_SIZE}.csv
                    done
                done
            done
        fi
    done
done




# touch scratch/$filename
