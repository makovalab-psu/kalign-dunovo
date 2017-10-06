SOURCES = kalign2_advanced_gaps.c \
          kalign2_alignment_types.c \
          kalign2_distance_calculation.c \
          kalign2_dp.c \
          kalign2_feature.c \
          kalign2_hirschberg.c \
          kalign2_hirschberg_dna.c \
          kalign2_inferface.c \
          kalign2_input.c \
          kalign2_main.c \
          kalign2_mem.c \
          kalign2_misc.c \
          kalign2_output.c \
          kalign2_profile_alignment.c \
          kalign2_profile.c \
          kalign2_string_matching.c \
          kalign2_tree.c
CC = gcc
CFLAGS = -O9 -Wall -fPIC
OBJECTS = $(SOURCES:.c=.o)

.PHONY: all clean

all: $(OBJECTS)
	$(CC) $(CFLAGS) -shared $(OBJECTS) -o libkalign.so

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f kalign.so $(OBJECTS)
