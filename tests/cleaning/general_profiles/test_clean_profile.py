from votekit.pref_profile import PreferenceProfile, CleanedProfile
from votekit.ballot import Ballot
from votekit.cleaning import clean_profile

profile = PreferenceProfile(
    ballots=[
        Ballot(ranking=[{"A"}, {"B"}], weight=1),
        Ballot(ranking=[{"A"}, {"B"}, {"C"}], weight=1),
        Ballot(ranking=[{"C"}, {"B"}, {"A"}], weight=3),
        Ballot(ranking=({"A"},)),
        Ballot(ranking=({"B"},), weight=0),
    ]
)


def test_clean_profile_with_defaults():
    adj_profile = clean_profile(
        profile,
        lambda x: Ballot(
            ranking=[c_set for c_set in x.ranking if "A" not in c_set], weight=x.weight
        ),
    )

    assert isinstance(adj_profile, CleanedProfile)
    assert adj_profile.parent_profile == profile
    assert adj_profile.ballots == (
        Ballot(ranking=[{"B"}], weight=1),
        Ballot(ranking=[{"B"}, {"C"}], weight=1),
        Ballot(ranking=[{"C"}, {"B"}], weight=3),
    )
    assert adj_profile != profile

    assert adj_profile.no_wt_altr_idxs == set()
    assert adj_profile.no_rank_no_score_altr_idxs == {3}
    assert adj_profile.nonempty_altr_idxs == {0, 1, 2}
    assert adj_profile.unaltr_idxs == {4}


def test_clean_profile_change_defaults():
    adj_profile = clean_profile(
        profile,
        lambda x: Ballot(
            ranking=[c_set.difference({"A"}) for c_set in x.ranking],
            weight=x.weight,
        ),
        remove_empty_ballots=False,
        remove_zero_weight_ballots=False,
        retain_original_candidate_list=True,
        retain_original_max_ranking_length=False,
    )
    assert isinstance(adj_profile, CleanedProfile)
    assert adj_profile.parent_profile == profile
    assert set(adj_profile.ballots) == set(
        (
            Ballot(ranking=[frozenset(), {"B"}], weight=1),
            Ballot(ranking=[frozenset(), {"B"}, {"C"}], weight=1),
            Ballot(
                ranking=[
                    {"C"},
                    {"B"},
                    frozenset(),
                ],
                weight=3,
            ),
            Ballot(ranking=(frozenset(),)),
            Ballot(ranking=({"B"},), weight=0),
        )
    )

    assert adj_profile.candidates == profile.candidates
    assert adj_profile.max_ranking_length == 3
    assert adj_profile.no_wt_altr_idxs == set()
    assert adj_profile.no_rank_no_score_altr_idxs == set()
    assert adj_profile.nonempty_altr_idxs == {0, 1, 2, 3}
    assert adj_profile.unaltr_idxs == {4}
