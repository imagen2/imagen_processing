#!/usr/bin/env python3

from typing import (
    Any,
    Callable,
    Match,
    Sequence,
)

from dataclasses import dataclass, field
import re
from operator import attrgetter
import logging
from pathlib import Path
from statistics import mean

import pandas as pd
from halfpipe.ingest.glob import tag_glob

logger = logging.getLogger()

subject_regex = r"[0-9]{12}"
session_regex = r"(?:bl|fu2|fu3)"


def merge(*args: dict) -> dict:
    c = dict()
    for a in args:
        c.update(a)
    return c


def cleaner(y: str) -> str:
    return "".join([x for x in y if x.isalnum()])


def check_readable(file_path: Path) -> bool:
    try:
        with open(file_path) as file_handle:
            assert len(file_handle.readlines()) > 0
        return True
    except Exception:
        return False


def path_pattern(task_short_name: str) -> str:
    return (
        f"./nifti/{{sub:{subject_regex}}}/BehaviouralData/"
        f"{task_short_name}_{{sub:{subject_regex}}}*.csv"
    )


@dataclass
class Event:
    stimulus: str
    onset: float
    duration: float | str
    reaction_time: float | None = None
    response: str | None = None


@dataclass
class Column:
    index: int | None
    name: str | None

    action: str
    args: dict


@dataclass
class Action:
    name: str
    args: dict


@dataclass
class Record:
    id: str
    pattern: str | None = None
    wildcard: str | None = None
    literal: str | None = None
    type: str | None = None


@dataclass
class Line:
    records: Sequence[str | None]
    update: Callable[[dict, Match], dict] | None = None
    factory: Callable[[dict, Match], list[Event]] | None = None


@dataclass
class PathSpec:
    path_patterns: list[str]
    filters: list[Callable[[list[tuple[Path, dict]]], list[tuple[Path, dict]]]] = field(
        default_factory=list
    )


@dataclass
class LogFile:
    task_name: str
    path_specs: list[PathSpec]

    sep: str

    records: list[Record]
    lines: list[Line]


faces_log_file = LogFile(
    task_name="faces",
    path_specs=[
        PathSpec(
            path_patterns=[
                path_pattern("ft"),
            ],
            filters=[],
        ),
    ],
    sep="\t",
    records=[
        Record(id="onset", type="int"),
        Record(id="video_clip_angry", pattern=r".+faces_a[1-5]\.mpg"),
        Record(id="video_clip_happy", pattern=r".+faces_h[1-5]\.mpg"),
        Record(id="video_clip_neutral", pattern=r".+faces_n[1-5]\.mpg"),
        Record(id="video_clip_control", pattern=r".+control\.mpg"),
    ],
    lines=[
        Line(
            records=["onset", "video_clip_angry"],
            factory=lambda _, groupdict: [
                Event(
                    stimulus="clip_faces_angry",
                    onset=float(groupdict["onset"]) / 1e3,
                    duration=18.0,
                ),
            ],
        ),
        Line(
            records=["onset", "video_clip_happy"],
            factory=lambda _, groupdict: [
                Event(
                    stimulus="clip_faces_happy",
                    onset=float(groupdict["onset"]) / 1e3,
                    duration=18.0,
                ),
            ],
        ),
        Line(
            records=["onset", "video_clip_neutral"],
            factory=lambda _, groupdict: [
                Event(
                    stimulus="clip_faces_neutral",
                    onset=float(groupdict["onset"]) / 1e3,
                    duration=18.0,
                ),
            ],
        ),
        Line(
            records=["onset", "video_clip_control"],
            factory=lambda _, groupdict: [
                Event(
                    stimulus="clip_concentric_circles",
                    onset=float(groupdict["onset"]) / 1e3,
                    duration=18.0,
                ),
            ],
        ),
    ],
)


mid_log_file = LogFile(
    task_name="mid",
    path_specs=[
        PathSpec(
            path_patterns=[
                path_pattern("mid"),
            ],
            filters=[],
        ),
    ],
    sep="\t",
    records=[
        Record(id="trial_type", pattern=r"(?:BIG_WIN|SMALL_WIN|NO_WIN)"),
        Record(id="trial_onset", type="int"),
        Record(id="target_onset", type="int"),
        Record(id="target_duration", type="int"),
        Record(id="outcome", pattern=r"(?:SUCCESS|FAILURE)"),
        Record(id="feedback_onset", type="int"),
        Record(id="fixation_onset", type="int"),
    ],
    lines=[
        Line(
            records=[
                None,
                "trial_type",
                "trial_onset",
                None,
                None,
                None,
                None,
                "target_onset",
                "target_duration",
                None,
                None,
                "feedback_onset",
                "outcome",
                None,
                "fixation_onset",
            ],
            factory=lambda _, groupdict: [
                Event(
                    stimulus=("cue_anticipation_" + groupdict["trial_type"].lower()),
                    onset=float(groupdict["trial_onset"]) / 1e3,
                    duration="until_next_target",
                ),
                Event(
                    stimulus="target",
                    onset=float(groupdict["target_onset"]) / 1e3,
                    duration=float(groupdict["target_duration"]) / 1e3,
                ),
                Event(
                    stimulus=(
                        dict(SUCCESS="feedback_", FAILURE="feedback_no_")[
                            groupdict["outcome"]
                        ]
                        + groupdict["trial_type"].lower()
                    ).replace("no_no", "no"),
                    onset=float(groupdict["feedback_onset"]) / 1e3,
                    duration=float(
                        int(groupdict["fixation_onset"])
                        - int(groupdict["feedback_onset"])
                    )
                    / 1e3,
                ),
            ],
        ),
    ],
)

stop_signal_log_file = LogFile(
    task_name="stop_signal",
    path_specs=[
        PathSpec(
            path_patterns=[
                path_pattern("ss"),
            ],
            filters=[],
        ),
    ],
    sep="\t,",
    records=[
        Record(
            id="trial_type",
            pattern=(
                r"\"?(?:GO_SUCCESS|GO_TOO_LATE|GO_WRONG_KEY_RESPONSE|"
                r"STOP_SUCCESS|STOP_FAILURE|STOP_TOO_EARLY_RESPONSE)\"?"
            ),
        ),
        Record(id="trial_onset", type="int"),
    ],
    lines=[
        Line(
            records=[
                None,  # Trial
                None,  # Trial Category
                None,  # Trial Start Time (Onset)
                None,  # Pre-determined/randomised onset
                "trial_onset",  # Go Stimulus Presentation Time
                None,  # Stimulus Presented
                None,  # Delay
                None,  # Stop Stimulus Presentation Time
                None,  # Response made by subject
                None,  # Absolute Response Time
                None,  # Relative Response Time
                "trial_type",  # Response Outcome
                None,  # Real Jitter
                None,  # Pre-determined Jitter
                None,  # Success Rate of Variable Delay Stop Trials
                None,  # Scanner Pulse'
            ],
            factory=lambda _, groupdict: [
                Event(
                    stimulus=groupdict["trial_type"].lower().strip('"'),
                    onset=float(groupdict["trial_onset"]) / 1e3,
                    duration=0.0,
                ),
            ],
        ),
    ],
)


def get_log_file_matchfuns(log_file: LogFile) -> list[Callable]:
    records: dict[str | None, str] = {None: f"[^{log_file.sep}]*"}
    for record in log_file.records:
        if record.type is not None:
            records[record.id] = {
                "int": r"-?\d+",
                "float": r"-?\d+(?:\.\d+)?",
                "str": "[a-zA-Z0-9_]+",
            }[record.type]
        elif record.pattern is not None:
            records[record.id] = record.pattern
        elif record.literal is not None:
            records[record.id] = re.escape(record.literal)
        else:
            raise ValueError()
    matchfuns = []
    for line in log_file.lines:
        pattern = ""
        for record_id in line.records:
            if len(pattern) > 0 and pattern[-1] != log_file.sep:
                pattern += f"[{log_file.sep}]"
            if record_id is None:
                pattern += records[None]
            else:
                pattern += f"(?P<{record_id}>{records[record_id]})"
        print(repr(pattern))
        matchfuns.append(re.compile(pattern).search)
    return matchfuns


def process_log_files(log_file: LogFile):
    matchfuns = get_log_file_matchfuns(log_file)

    log_file_paths_by_subject: dict[tuple[str, str], list[Path]] = dict()

    for path_spec in log_file.path_specs:
        path_tuples = list()
        for path_pattern in path_spec.path_patterns:
            for path_str, tag_dict in tag_glob(path_pattern, entities=["sub"]):
                path_tuples.append((Path(path_str), tag_dict))
        for filter_fun in path_spec.filters:
            path_tuples = filter_fun(path_tuples)

        for log_file_path, tag_dict in path_tuples:
            index = tag_dict["sub"]
            if index not in log_file_paths_by_subject:
                log_file_paths_by_subject[index] = list()
            log_file_paths_by_subject[index].append(log_file_path)

    for subject, log_file_paths in log_file_paths_by_subject.items():
        base_dir = Path("/mnt/datasets/stratify/events/")
        subject_dir = f"{subject}"

        (base_dir / subject_dir).mkdir(parents=True, exist_ok=True)
        out_path = base_dir / subject_dir / f"{log_file.task_name}.tsv"

        rows = list()
        for file_path in log_file_paths:
            try:
                with open(file_path, "r") as file_handle:
                    rows.extend(file_handle.readlines())
            except Exception as e:
                logger.warning(f"Cannot read file {file_path}", exc_info=e)

        context: dict[str, Any] = dict()
        events = dict()

        # import pdb; pdb.set_trace()

        for row in rows:
            for i, line in enumerate(log_file.lines):
                m = matchfuns[i](row)
                if m is not None:
                    try:
                        groupdict = m.groupdict()
                        if line.update is not None:
                            context.update(line.update(context, groupdict))
                        if line.factory is not None:
                            events.update(
                                {
                                    f"{event.onset:06.2f}": event
                                    for event in line.factory(context, groupdict)
                                }
                            )
                    except Exception as e:
                        # import pdb; pdb.set_trace()
                        logger.warning(
                            "Error reading log files "
                            f"{log_file_paths} for subject {subject}",
                            exc_info=e,
                        )

        events_list = sorted(events.values(), key=attrgetter("onset"))
        if len(events_list) == 0:
            logger.warning(
                f"Could not find any events for subject {subject} and "
                f"files {log_file_paths}"
            )
            continue

        trial_types = list()
        onsets = list()
        durations: list[float] = list()
        responses = list()

        for i, event in enumerate(events_list):
            trial_types.append(event.stimulus)
            onsets.append(event.onset)

            duration = event.duration
            if isinstance(duration, str):
                tokens = duration.split("_")
                assert tokens[0] == "until"
                assert tokens[1] == "next"
                match_stimuli = set(token for token in tokens[2:] if token != "or")
                for j in range(i + 1, len(events_list)):
                    if (
                        events_list[j].stimulus in match_stimuli
                        or len(match_stimuli) == 0
                    ):
                        duration = events_list[j].onset - event.onset
                        break

                if isinstance(duration, str):  # last block
                    if isinstance(events_list[-1].duration, float):
                        duration = (
                            events_list[-1].onset
                            + events_list[-1].duration
                            - event.onset
                        )
                    elif "end" in context:
                        duration = context["end"]
                    else:
                        duration = mean(
                            d
                            for trial_type, d in zip(trial_types, durations)
                            if trial_type == event.stimulus
                        )
                        logger.warning(
                            "Inferred duration for last event "
                            f'"{event.stimulus}" '
                            "to be average of other events of same type "
                            f"({duration} s)"
                        )

            assert isinstance(duration, float)
            durations.append(duration)

            responses.append(event.response)

        data_frame = pd.DataFrame(
            list(zip(trial_types, onsets, durations, responses)),
            columns=["trial_type", "onset", "duration", "response"],
        )

        data_frame = data_frame.dropna(axis=1, how="all")

        data_frame.to_csv(out_path, sep="\t", index=False, header=True, na_rep="n/a")
        logger.warning(f"Writing file {out_path}")


if __name__ == "__main__":
    process_log_files(mid_log_file)
    process_log_files(faces_log_file)
    process_log_files(stop_signal_log_file)
