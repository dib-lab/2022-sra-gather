# utility functions that I expect will come in handy in many analysis notebooks

read_gather <- function(path){
  gather <- read_csv(path, col_types = "ddddddddcccddddcccd")
}


