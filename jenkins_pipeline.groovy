pipeline {
    agent any 
    stages {
        stage('Build') { 
            steps {
                echo "building";
            }
        }
        stage('Test') { 
            steps {
                echo "test stage";
            }
        }
        stage('Deploy') { 
            steps {
                echo "deploy stage";
            }
        }
    }
}
