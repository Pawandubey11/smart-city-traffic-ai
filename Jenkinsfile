pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        PYTHONPATH = '.'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Environment & Dependencies Setup') {
            steps {
                sh '''
                    echo "Setting up Python virtual environment..."
                    python3 -m venv venv || virtualenv venv
                    . venv/bin/activate
                    pip install --upgrade pip setuptools wheel
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automated System Test Suites') {
            steps {
                sh '''
                    echo "Executing Smart City Traffic AI Test Suites..."
                    . venv/bin/activate
                    PYTHONPATH=. python3 tests/test_phase1_environment.py
                    PYTHONPATH=. python3 tests/test_phase2_video_pipeline.py
                    PYTHONPATH=. python3 tests/test_phase3_vehicle_detection.py
                    PYTHONPATH=. python3 tests/test_phase4_tracking.py
                    PYTHONPATH=. python3 tests/test_phase5_traffic_analysis.py
                    PYTHONPATH=. python3 tests/test_phase6_accident_ai.py
                    PYTHONPATH=. python3 tests/test_phase7_local_prototype.py
                    PYTHONPATH=. python3 tests/test_phase20_alpr_speed.py
                    PYTHONPATH=. python3 tests/test_phase21_emergency_priority.py
                '''
            }
        }

        stage('Build Edge Docker Container') {
            steps {
                sh '''
                    echo "Building Smart City Edge AI Docker Container..."
                    docker build -t smartcity-edge-ai:latest -f edge/Dockerfile .
                '''
            }
        }
    }

    post {
        always {
            echo "Jenkins Build Complete."
        }
        success {
            echo "SUCCESS: Jenkins Pipeline Built & Tested Smart City Traffic AI Service Cleanly!"
        }
        failure {
            echo "FAILURE: Jenkins Build Failed. Check console log trace above for details."
        }
    }
}
