# for figuring out how many rounds it should take.
import logging


class analyser:
    def __init__(self):
        pass
    def analyse(self, configuration: str, pattern: str):
        slices = [configuration[i: i + len(pattern)] for i in range(0,len(configuration), len(pattern))]
        zeroes = [s.count('0') - pattern.count('0') for s in slices]
        cumulative_zero_counter = 0
        not_full_pass = 0
        full_passes_added = 1
        estimated_rounds_required = len(slices) - 1
        for i, z in enumerate(zeroes):
            cumulative_zero_counter = cumulative_zero_counter + z
            #print(z, end = ' ')
            logging.info('i:' + str(i % len(slices)) + '\tz:' + str(z) +  '\tc:' + str(cumulative_zero_counter))

            if cumulative_zero_counter < -(len(pattern) / 2):
                cumulative_zero_counter += int((len(pattern) / 2))
                logging.info('AH')
                not_full_pass = i

            if cumulative_zero_counter > (full_passes_added * int(len(pattern) / 2)):
                logging.info('OH')
                not_full_pass = i
                if cumulative_zero_counter >= ((full_passes_added + 1) * int(len(pattern) / 2)):
                    full_passes_added += 1

        estimated_rounds_required += not_full_pass
        print('\nestimated rounds: ', estimated_rounds_required)

def main():
    ## tester
    a = analyser()
    a.analyse('000000000000111111111111','000111')
