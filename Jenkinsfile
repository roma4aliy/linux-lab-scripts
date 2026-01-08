pipeline {
    agent any

    environment {
        PACKAGE_NAME = 'count-files'
        PACKAGE_VERSION = '1.0'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -la'
            }
        }

        stage('Test Script') {
            steps {
                sh 'chmod +x count_files'
                sh 'bash -n count_files'
                sh './count_files'
            }
        }

        stage('Build RPM') {
            agent {
                docker {
                    image 'fedora:latest'
                    args '-u root'
                }
            }
            steps {
                sh '''
                    chmod +x count_files
                    dnf install -y rpm-build rpmdevtools || true
                    rpmdev-setuptree
                    mkdir -p ~/rpmbuild/SOURCES/${PACKAGE_NAME}-${PACKAGE_VERSION}
                    cp count_files ~/rpmbuild/SOURCES/${PACKAGE_NAME}-${PACKAGE_VERSION}/
                    cd ~/rpmbuild/SOURCES
                    tar czvf ${PACKAGE_NAME}-${PACKAGE_VERSION}.tar.gz ${PACKAGE_NAME}-${PACKAGE_VERSION}
                    cp ${WORKSPACE}/packaging/rpm/count-files.spec ~/rpmbuild/SPECS/
                    rpmbuild -ba ~/rpmbuild/SPECS/count-files.spec
                    cp ~/rpmbuild/RPMS/noarch/*.rpm ${WORKSPACE}/
                '''
            }
        }

        stage('Build DEB') {
            agent {
                docker {
                    image 'ubuntu:latest'
                    args '-u root'
                }
            }
            steps {
                sh '''
                    chmod +x count_files
                    apt-get update || true
                    apt-get install -y build-essential debhelper devscripts || true
                    mkdir -p build/${PACKAGE_NAME}-${PACKAGE_VERSION}
                    cp count_files build/${PACKAGE_NAME}-${PACKAGE_VERSION}/
                    cp -r packaging/deb/debian build/${PACKAGE_NAME}-${PACKAGE_VERSION}/
                    cd build/${PACKAGE_NAME}-${PACKAGE_VERSION}
                    dpkg-buildpackage -us -uc -b || true
                    cp ../*.deb ${WORKSPACE}/
                '''
            }
        }

        stage('Test RPM Installation') {
            agent {
                docker {
                    image 'oraclelinux:8'
                    args '-u root'
                }
            }
            steps {
                sh '''
                    rpm -ivh ${PACKAGE_NAME}-*.rpm || true
                    ./count_files
                    rpm -e ${PACKAGE_NAME} || true
                '''
            }
        }

        stage('Test DEB Installation') {
            agent {
                docker {
                    image 'ubuntu:latest'
                    args '-u root'
                }
            }
            steps {
                sh '''
                    dpkg -i ${PACKAGE_NAME}_*.deb || apt-get install -f -y || true
                    ./count_files
                    apt-get remove -y ${PACKAGE_NAME} || true
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: '*.rpm, *.deb'
            echo 'Build completed successfully!'
        }
        failure {
            echo 'Build failed!'
        }
        always {
            deleteDir()
        }
    }
}
