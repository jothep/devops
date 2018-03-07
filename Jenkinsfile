node {
	
    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */
	git https://github.com/jothep/devops.git
        docker.build("jasko/appwar")
    }

}
