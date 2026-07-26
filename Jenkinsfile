pipeline {
    agent any

    tools {
        // Verifica que este nombre coincida con tu configuración global de Jenkins
        jdk 'JDK21'
    }

    stages {
        stage('Stage 1: Ejecución Serenity') {
            steps {
                script {
                    echo '--- Descargando Proyecto Serenity BDD ---'
                    // Usamos un bloque limpio para clonar la URL del repositorio directamente
                    dir('proyecto-serenity') {
                        git branch: 'main', url: 'https://github.com'
                        
                        echo '--- Ejecutando Pruebas de Serenity BDD ---'
                        // Al estar en Windows (según tus logs), usamos bat obligatoriamente
                        bat 'gradlew.bat clean test aggregate'
                    }
                }
            }
            post {
                always {
                    dir('proyecto-serenity') {
                        // Publica el reporte nativo de Serenity HTML si es que se generó
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
                        git branch: 'main', url: 'https://github.com'
                        
                        echo '--- Ejecutando Pruebas de Playwright ---'
                        bat 'gradlew.bat test'
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