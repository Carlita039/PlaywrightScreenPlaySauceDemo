pipeline {
    agent any

    tools {
        // Este nombre debe coincidir EXACTAMENTE con el que configures en Jenkins
        jdk 'JDK21'
    }

    environment {
        REPO_SERENITY   = 'https://github.com'
        REPO_PLAYWRIGHT  = 'https://github.com'
    }

    stages {
        stage('Stage 1: Ejecución Serenity') {
            steps {
                script {
                    echo '--- Descargando Proyecto Serenity BDD ---'
                    dir('proyecto-serenity') {
                        git url: "${env.REPO_SERENITY}", branch: 'main'
                        
                        echo '--- Ejecutando Pruebas de Serenity BDD ---'
                        // En Windows se usa bat, en Linux/Mac se usa sh
                        if (isUnix()) {
                            sh 'chmod +x gradlew'
                            sh './gradlew clean test aggregate'
                        } else {
                            bat 'gradlew.bat clean test aggregate'
                        }
                    }
                }
            }
            post {
                always {
                    dir('proyecto-serenity') {
                        // Publica el reporte nativo de Serenity HTML
                        publishHTML([
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: 'target/site/serenity',
                            reportFiles: 'index.html',
                            reportName: 'Reporte Serenity BDD'
                        ])
                    }
                }
            }
        }

        stage('Stage 2: Ejecución Playwright') {
            steps {
                script {
                    echo '--- Descargando Proyecto Playwright Python ---'
                    dir('proyecto-playwright') {
                        git url: "${env.REPO_PLAYWRIGHT}", branch: 'main'
                        
                        echo '--- Ejecutando Pruebas de Playwright ---'
                        if (isUnix()) {
                            sh 'chmod +x gradlew'
                            sh './gradlew test'
                        } else {
                            bat 'gradlew.bat test'
                        }
                    }
                }
            }
            post {
                always {
                    dir('proyecto-playwright') {
                        // Publica los resultados para Allure
                        allure includeProperties: false, results: [[path: 'allure-results']]
                    }
                }
            }
        }
    }
}