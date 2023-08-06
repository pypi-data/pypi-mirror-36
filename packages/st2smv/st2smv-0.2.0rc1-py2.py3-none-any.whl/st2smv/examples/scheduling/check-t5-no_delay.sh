
st2smv --check-schedule \
    --input schedule-t5.json state-t5-no_delay.json \
    --metadata metadata.json \
    --output-directory results-t5_no_delay \
    --verbosity debug \
    --solver-path SynthSMV \
;
