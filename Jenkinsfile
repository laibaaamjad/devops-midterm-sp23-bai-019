pipeline {
  agent any
  triggers { githubPush() }
  environment {
    REG   = 'SP23-BAI-019'
    IMAGE = 'midterm-sp23-bai-019'
  }
  stages {
    stage('Fetch latest data') {
      steps {
        checkout scm
        sh 'wc -l dataset/train.csv'
      }
    }
    stage('Train') {
      steps {
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install -q -r requirements.txt
          python train.py
        '''
      }
    }
    stage('Test') {
      steps {
        sh '. venv/bin/activate && pytest -q'
      }
    }
    stage('Docker build') {
      steps {
        sh "docker build --build-arg BUILD_COMMIT=${env.GIT_COMMIT} -t ${IMAGE}:${env.BUILD_NUMBER} -t ${IMAGE}:latest ."
      }
    }
    stage('Deploy on EC2') {
      steps {
        sh """
          docker rm -f ${IMAGE} || true
          docker run -d --name ${IMAGE} --restart unless-stopped -p 8000:8000 ${IMAGE}:latest
          for i in 1 2 3 4 5 6 7 8 9 10; do
            curl -sf http://localhost:8000/metrics > metrics_out.json && break || sleep 2
          done
        """
      }
    }
  }
  post {
    always {
      script {
        def m = fileExists('metrics_out.json') ? readFile('metrics_out.json') : 'n/a'
        emailext(
          from: 'laibiioye22@gmail.com',
          to: 'qasimalik@gmail.com',
          subject: "[${REG}] Retrain pipeline #${env.BUILD_NUMBER}: ${currentBuild.currentResult}",
          body: "Student Reg No: ${REG}\nResult: ${currentBuild.currentResult}\nCommit: ${env.GIT_COMMIT}\nMetrics: ${m}\nBuild: ${env.BUILD_URL}"
        )
      }
    }
  }
}