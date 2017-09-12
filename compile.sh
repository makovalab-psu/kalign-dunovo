set -e
gcc -O9 -Wall -fPIC -c kalign2_distance_calculation.c
gcc -O9 -Wall -fPIC -c kalign2_dp.c
gcc -O9 -Wall -fPIC -c kalign2_input.c
gcc -O9 -Wall -fPIC -c kalign2_main.c
gcc -O9 -Wall -fPIC -c kalign2_mem.c
gcc -O9 -Wall -fPIC -c kalign2_inferface.c
gcc -O9 -Wall -fPIC -c kalign2_misc.c
gcc -O9 -Wall -fPIC -c kalign2_tree.c
gcc -O9 -Wall -fPIC -c kalign2_profile.c
gcc -O9 -Wall -fPIC -c kalign2_alignment_types.c
gcc -O9 -Wall -fPIC -c kalign2_feature.c
gcc -O9 -Wall -fPIC -c kalign2_hirschberg.c
gcc -O9 -Wall -fPIC -c kalign2_advanced_gaps.c
gcc -O9 -Wall -fPIC -c kalign2_hirschberg_dna.c
gcc -O9 -Wall -fPIC -c kalign2_output.c
gcc -O9 -Wall -fPIC -c kalign2_string_matching.c
gcc -O9 -Wall -fPIC -c kalign2_profile_alignment.c
gcc -O9 -Wall -shared -fPIC kalign2_distance_calculation.o kalign2_dp.o kalign2_input.o kalign2_main.o kalign2_mem.o kalign2_inferface.o kalign2_misc.o kalign2_tree.o kalign2_profile.o kalign2_alignment_types.o kalign2_feature.o kalign2_hirschberg.o kalign2_advanced_gaps.o kalign2_hirschberg_dna.o kalign2_output.o kalign2_string_matching.o kalign2_profile_alignment.o -o kalign.so
