# Basic simple test of stack-orchestrator functionality
echo "Running stack-orchestrator smoke test"
# Bit of a hack, test the most recent package
TEST_TARGET_SO=$( ls -t1 ./package/laconic-so* | head -1 )
# Set a non-default repo dir
export CERC_REPO_BASE_DIR=~/stack-orchestrator-test/repo-base-dir
echo "Testing this package: $TEST_TARGET_SO"
echo "Test version command"
reported_version_string=$( $TEST_TARGET_SO version )
echo "Version reported is: ${reported_version_string}"
echo "Cloning repositories into: $CERC_REPO_BASE_DIR"
rm -rf $CERC_REPO_BASE_DIR
mkdir -p $CERC_REPO_BASE_DIR
# Pull an example small public repo to test we can pull a repo
$TEST_TARGET_SO setup-repositories --include cerc-io/laconic-sdk
# Test pulling a stack
$TEST_TARGET_SO --stack test setup-repositories
# Test building the a stack container
$TEST_TARGET_SO --stack test build-containers
# Build one example containers
$TEST_TARGET_SO build-containers --include cerc/builder-js
# Deploy the test container
$TEST_TARGET_SO --stack test deploy-system up
# TODO: test that we can use the deployed container somehow
# Clean up
$TEST_TARGET_SO --stack test deploy-system down
echo "Test passed"
