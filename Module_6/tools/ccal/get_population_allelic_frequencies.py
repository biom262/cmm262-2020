from warnings import warn


def get_population_allelic_frequencies(caf):

    try:

        return [
            float(population_allelic_frequency)
            for population_allelic_frequency in caf.split(sep=",")
        ]

    except ValueError:

        warn("Bad CAF {}.".format(caf))

        return [
            float(population_allelic_frequency)
            for population_allelic_frequency in caf.split(sep=",")
            if population_allelic_frequency and population_allelic_frequency != "."
        ]
