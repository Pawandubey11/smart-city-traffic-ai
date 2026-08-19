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
                    echo "Setting up Python environment..."
                    python3 -m venv venv || python3 -m venv --without-pip venv || true
                    
                    if [ -f venv/bin/python3 ]; then
                        echo "Virtual environment created at ./venv"
                        if [ ! -f venv/bin/pip ]; then
                            echo "Installing pip into venv..."
                            curl -sS https://bootstrap.pypa.io/get-pip.py | ./venv/bin/python3 || true
                        fi
                        . venv/bin/activate
                        pip install --upgrade pip setuptools wheel --quiet || true
                        pip install -r requirements.txt
                    else
                        echo "Fallback to user-level pip installation..."
                        python3 -m pip install --user --upgrade pip || true
                        python3 -m pip install --user -r requirements.txt
                    fi
                '''
            }
        }

        stage('Run Automated System Test Suites') {
            steps {
                sh '''
                    echo "Executing Smart City Traffic AI Test Suites..."
                    if [ -f venv/bin/activate ]; then
                        . venv/bin/activate
                    fi
                    python3 tests/test_phase1_environment.py
                    python3 tests/test_phase2_video_pipeline.py
                    python3 tests/test_phase3_vehicle_detection.py
                    python3 tests/test_phase4_tracking.py
                    python3 tests/test_phase5_traffic_analysis.py
                    python3 tests/test_phase6_accident_ai.py
                    python3 tests/test_phase7_local_prototype.py
                    python3 tests/test_phase20_alpr_speed.py
                    python3 tests/test_phase21_emergency_priority.py
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
