from votekit.cvr_loaders import load_blt
import votekit.cleaning as clean
from votekit.election_state import ElectionState

import votekit.ballot_generator as bg
import votekit.election_types as elections
from pathlib import Path

# TODO:
# need to do one with visualizations,
# need to test other elections,
# need to test cleaning methods,
# need to add cleaning methods (ballot truncation for ex)
# need to test ballot generation models


def test_load_clean_completion():
    """simple example of what a "full" use would look like"""

    # load CVR -> PP representation
    BASE_DIR = Path(__file__).resolve().parent
    BLT_DIR = BASE_DIR / "data/txt/"

    pp, seats = load_blt(BLT_DIR / "edinburgh17-01_abridged.blt")
    print(pp)

    # apply rules to get new PP
    cleaned_pp = clean.remove_noncands(pp, ["Graham HUTCHISON (C)"])

    # write intermediate output for inspection
    # cleaned_pp.save("cleaned.cvr")

    # run election using a configured RCV step object
    election_borda = elections.Borda(cleaned_pp, 1, score_vector=None)

    outcome_borda = election_borda.run_election()

    assert isinstance(outcome_borda, ElectionState)

    # plot_results(outcome)


def test_generate_election_completion():

    number_of_ballots = 100
    candidates = ["W1", "W2", "C1", "C2"]
    slate_to_candidate = {"W": ["W1", "W2"], "C": ["C1", "C2"]}
    bloc_crossover_rate = {"W": {"C": 0.3}, "C": {"W": 0.4}}
    pref_interval_by_bloc = {
        "W": {"W1": 0.4, "W2": 0.3, "C1": 0.2, "C2": 0.1},
        "C": {"W1": 0.2, "W2": 0.2, "C1": 0.3, "C2": 0.3},
    }
    bloc_voter_prop = {"W": 0.7, "C": 0.3}

    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data/"
    path = Path(DATA_DIR, "Cambridge_09to17_ballot_types.p")

    ballot_model = bg.CambridgeSampler(
        candidates=candidates,
        pref_interval_by_bloc=pref_interval_by_bloc,
        bloc_voter_prop=bloc_voter_prop,
        path=path,
        bloc_crossover_rate=bloc_crossover_rate,
        slate_to_candidates=slate_to_candidate,
    )

    pp = ballot_model.generate_profile(number_of_ballots=number_of_ballots)

    election_borda = elections.Borda(pp, 1, score_vector=None)

    outcome_borda = election_borda.run_election()

    assert isinstance(outcome_borda, ElectionState)
