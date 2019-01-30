#jenkins use kubernetes-plugin , use pod of multi containers to build ,accese to aws eks and ecr(docker registry)

pipeline{
    agent {
      node {
        label 'jasko-jnlp'
      }
    }
    tools{
        maven 'maven'
        jdk 'JDK_8'
    }
    stages {
        stage ("initialize") {
            steps {
            checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/Wen-Xiu/dddsample.git']]])
                        }
            }
        stage ('mvn test'){
        //mvn 测试
            steps {
        sh "mvn test"
            }
    }

        stage ('mvn build'){
        //mvn构建
            steps {
        sh "mvn clean install -Dmaven.test.skip=true"
            }
    }
}
}
