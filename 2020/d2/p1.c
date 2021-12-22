#include <stdio.h>
#include <stdlib.h>

// Count the occurances of char_to_search in rest of line
int count_chars(char char_to_search, char *line)
{
  int counter = 0, i = 0;
  char c;
  while (c = line[i++])
    counter += (c == char_to_search);
  return counter;
}

// Check if a single password is valid
int check_one_password(char *line)
{
  int i = 0; // counter for place in the char array

  // This is a little hack since atoi stops after the first non-digit
  int lower_bound = atoi(line);
  while (line[i++] != '-')
    ; // fast forward to the next number
  int upper_bound = atoi(&line[i]);
  while (line[i++] != ' ')
    ; // fast forward to the char_to_search

  int count = count_chars(line[i], &line[i + 2]);
  return (lower_bound <= count && count <= upper_bound);
}

int part_one(char *filename)
{
  FILE *fp;
  fp = fopen(filename, "r");

  int result = 0;
  char line[64];
  while (fgets(line, 64, fp) != NULL)
  {
    result += check_one_password(line);
  }
  fclose(fp);

  return result;
}

int main(int argc, char *argv[])
{
  printf("%d\n", part_one(argv[1]));
}