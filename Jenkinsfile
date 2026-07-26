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
                    
                    bat "if exist proyecto-serenity rmdir /s /q proyecto-serenity"
                    
                    bat """
                        set DOMAIN=https://github.com
                        set REPO=/Carlita039/proyectoSerenityBDD.git
                        git clone -b main %DOMAIN%%REPO% proyecto-serenity
                    """
                    
                    dir('proyecto-serenity') {
                        echo '--- Restaurando Gradle Wrapper ---'
                        // Si tienes Gradle instalado en tu laptop, este comando generará el .jar faltante
                        bat "gradle wrapper"
                        
                        echo '--- Ejecutando Pruebas de Serenity BDD ---'
                        bat "gradlew.bat clean test aggregate"
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
                    
                    bat "if exist proyecto-playwright rmdir /s /q proyecto-playwright"
                    
                    bat """
                        set DOMAIN=https://github.com
                        set REPO=/Carlita039/PlaywrightScreenPlaySauceDemo.git
                        git clone -b main %DOMAIN%%REPO% proyecto-playwright
                    """
                    
                    dir('proyecto-playwright') {
                        echo '--- Restaurando Gradle Wrapper ---'
                        bat "gradle wrapper"
                        
                        echo '--- Ejecutando Pruebas de Playwright ---'
                        bat "gradlew.bat test"
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