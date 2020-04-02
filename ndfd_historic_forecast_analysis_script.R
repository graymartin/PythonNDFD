# ndfd historic forecast analysis script

# ---- To Do List ----
# TODO for now set date as character but figure out why ymd_hm("2016-01-01 00:00", tz = "UCT") gives result without time but ymd_hm("2016-01-01 13:00", tz = "UCT") gives it with the time
# TODO need to loop through all 1095 days


# ---- load libraries ----
library(tidyverse)
library(here)
library(lubridate)


# ---- load data ----
# path to data from the sco
ndfd_sco_data_path <- "/Users/sheila/Documents/bae_shellcast_project/shellcast_analysis/ndfd_get_data/data/ndfd_sco_data/"

# historic data
ndfd_hist_pop12_data_raw <- read_csv(paste0(ndfd_sco_data_path, "pop12_2016010100.csv"),
                                     col_types = list(col_double(), col_double(), col_double(), col_double(), col_double(), col_double(), col_double(),
                                                      col_character(), col_character(), col_character(), col_character(), col_character()))
ndfd_hist_qpf_data_raw <- read_csv(paste0(ndfd_sco_data_path, "qpf_2016010100.csv"),
                                   col_types = list(col_double(), col_double(), col_double(), col_double(), col_double(), col_double(), col_double(),
                                                    col_character(), col_character(), col_character(), col_character(), col_character()))


# ---- wrangle data ----
# wrangle
ndfd_hist_pop12_data <- ndfd_hist_pop12_data_raw %>%
  select(x_index, y_index, latitude, longitude, time_uct, time_nyc, pop12_value_perc, valid_period_hrs)
ndfd_hist_qpf_data <- ndfd_hist_qpf_data_raw %>%
  select(x_index, y_index, latitude, longitude, time_uct, time_nyc, qpf_value_kmperm2, valid_period_hrs) %>%
  mutate(qpf_value_in = qpf_value_kmperm2 * (1/1000) * (100) * (1/2.54)) # convert to inches, density of water is 1000 kg/m3

# select only 12 hr output
ndfd_hist_pop12_data_12hr <- ndfd_hist_pop12_data %>%
  filter(valid_period_hrs == 12)
ndfd_hist_qpf_data_12hr <- ndfd_hist_qpf_data %>%
  filter(valid_period_hrs == 12)


# ---- plot data ----
# plot pop12 data
ggplot(data = ndfd_hist_pop12_data_12hr) +
  geom_point(aes(x = longitude, y = latitude, color = pop12_value_perc)) +
  scale_color_gradient(low = "white", high = "blue", na.value = "grey90", limits = c(0, 100))

# plot qpf data
#max(ndfd_hist_qpf_data$qpf_value_in, na.rm = TRUE)
ggplot(data = ndfd_hist_qpf_data_12hr) +
  geom_point(aes(x = longitude, y = latitude, color = qpf_value_in)) +
  scale_color_gradient(low = "white", high = "blue", na.value = "grey90", limits = c(0, 1))
