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
