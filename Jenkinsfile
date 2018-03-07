node {
	
    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */
	git url: 'https://github.com/jothep/devops.git'
        docker.build("jasko/appwar")
    }

	stage('Push image'){
	withCredentials([usernamePassword(credentialsId: 'dockerHub', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
          sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
          sh 'docker push jasko/appwar'
	}
	}
		
}
