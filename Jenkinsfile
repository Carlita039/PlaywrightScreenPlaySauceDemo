pipeline {
    agent any

    tools {
        jdk 'JDK21'
    }

    stages {
        stage('Stage 1: Ejecución Serenity') {
            steps {
                script {
                    echo '--- Preparando directorio y clonando Serenity BDD ---'
                    
                    // Borra la carpeta con error si es que existe en Windows
                    bat 'if exist proyecto-serenity rmdir /s /q proyecto-serenity'
                    
                    // Clonamos de forma directa usando la consola nativa de Windows
                    bat 'git clone -b main https://github.com proyecto-serenity'
                    
                    dir('proyecto-serenity') {
                        echo '--- Ejecutando Pruebas de Serenity BDD ---'
                        bat 'gradlew.bat clean test aggregate'
                    }
                }
            }
            post {
                always {
                    dir('proyecto-serenity') {
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
                    echo '--- Preparando directorio y clonando Playwright ---'
                    
                    bat 'if exist proyecto-playwright rmdir /s /q proyecto-playwright'
                    bat 'git clone -b main https://github.com proyecto-playwright'
                    
                    dir('proyecto-playwright') {
                        echo '--- Ejecutando Pruebas de Playwright ---'
                        bat 'gradlew.bat test'
                    }
                }
            }
            post {
                always {
                    dir('proyecto-playwright') {
                        allure includeProperties: false, results: [[path: 'allure-results']]
                    }
                }
            }
        }
    }
}