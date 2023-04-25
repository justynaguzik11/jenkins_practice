timeout(time: 15, unit: 'MINUTES') {
    node {
        try {
            stage('Checkout') {
                cleanWs()
                checkout(scm)
            }
            stage('Run') {
                docker.build('python-docker', ".").inside {
                    script {
                        cmd = "python3 client.py"
                        sh(script: cmd)
                    }
                }
            }
        } catch (err) {
            currentBuild.result = "FAILED"
            print 'Build failed'
            print err
        }
        finally {
            stage("Post-build") {
                script {
                    println "Post-build anyway"
                }
            cleanWs()
            }
        }
    }
}