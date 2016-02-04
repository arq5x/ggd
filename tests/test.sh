test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

source ssshtest

# set exit code on bad recipe
run test_bad_sha ggd install --cookbook file://$(pwd)/tests/ t1
assert_equal $RETVAL 4
assert_in_stderr "ERROR in sha1 check"

run test_good_sha ggd install --cookbook file://$(pwd)/tests/ t2
assert_equal $RETVAL 0
assert_in_stderr "validating"
assert_in_stderr "installed t2"
assert_in_stderr "no SHA1 provided for" # no sha for the 3rd file

run test_missing_software ggd install --cookbook file://$(pwd)/tests/ test-missing-software-deps
assert_equal $RETVAL 5

run test_has_software ggd install --cookbook file://$(pwd)/tests/ test-has-software-deps
assert_equal $RETVAL 0
