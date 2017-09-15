CC = gcc
CFLAGS = -O9 -Wall -fPIC

all:
	$(CC) $(CFLAGS) -c kalign2_distance_calculation.c
	$(CC) $(CFLAGS) -c kalign2_dp.c
	$(CC) $(CFLAGS) -c kalign2_input.c
	$(CC) $(CFLAGS) -c kalign2_main.c
	$(CC) $(CFLAGS) -c kalign2_mem.c
	$(CC) $(CFLAGS) -c kalign2_inferface.c
	$(CC) $(CFLAGS) -c kalign2_misc.c
	$(CC) $(CFLAGS) -c kalign2_tree.c
	$(CC) $(CFLAGS) -c kalign2_profile.c
	$(CC) $(CFLAGS) -c kalign2_alignment_types.c
	$(CC) $(CFLAGS) -c kalign2_feature.c
	$(CC) $(CFLAGS) -c kalign2_hirschberg.c
	$(CC) $(CFLAGS) -c kalign2_advanced_gaps.c
	$(CC) $(CFLAGS) -c kalign2_hirschberg_dna.c
	$(CC) $(CFLAGS) -c kalign2_output.c
	$(CC) $(CFLAGS) -c kalign2_string_matching.c
	$(CC) $(CFLAGS) -c kalign2_profile_alignment.c
	$(CC) $(CFLAGS) -shared kalign2_distance_calculation.o kalign2_dp.o kalign2_input.o kalign2_main.o kalign2_mem.o kalign2_inferface.o kalign2_misc.o kalign2_tree.o kalign2_profile.o kalign2_alignment_types.o kalign2_feature.o kalign2_hirschberg.o kalign2_advanced_gaps.o kalign2_hirschberg_dna.o kalign2_output.o kalign2_string_matching.o kalign2_profile_alignment.o -o kalign.so

clean:
	rm -f *.o *.so
