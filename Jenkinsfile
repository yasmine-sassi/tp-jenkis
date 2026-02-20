pipeline {
    // Exécuter le pipeline sur n'importe quel agent Jenkins disponible
    agent any

    environment {
        // Nom de l'image Docker sur Docker Hub : username/nom-repo
        DOCKER_IMAGE = "yasminesassi3/mon-app-devops"
        // Tag de l'image = numéro de build Jenkins (ex: 1, 2, 3...)
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {

        // =============================
        // STAGE 1 : Récupération du code
        // =============================
        stage('Checkout') {
            steps {
                echo 'Récupération du code source...'
                // Cloner le dépôt GitHub sur la branche main
                git branch: 'main', url: 'https://github.com/yasmine-sassi/tp-jenkis.git'
            }
        }

        // =============================
        // STAGE 2 : Tests unitaires
        // =============================
        stage('Unit Tests') {
            steps {
                echo 'Exécution des tests unitaires...'
                sh '''
                    # Créer un environnement virtuel Python isolé
                    python3 -m venv venv

                    # Activer l'environnement virtuel
                    . venv/bin/activate

                    # Installer les dépendances du projet
                    pip install -r requirements.txt

                    # Lancer les tests avec pytest
                    # Le pipeline s'arrête automatiquement si un test échoue
                    pytest test_app.py -v
                '''
            }
        }

        // =============================
        // STAGE 3 : Build de l'image Docker
        // =============================
        stage('Docker Build') {
            steps {
                echo "Construction de l'image Docker taguée ${BUILD_NUMBER}..."

                // Construire l'image avec le tag numéro de build (ex: yasminesassi3/mon-app-devops:3)
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."

                // Ajouter aussi le tag 'latest' sur la même image
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        // =============================
        // STAGE 4 : Publication sur Docker Hub
        // =============================
        stage('Docker Push') {
            steps {
                echo 'Connexion à Docker Hub et publication...'

                // Utiliser les credentials Jenkins stockés de façon sécurisée
                // Le mot de passe n'apparaît jamais en clair dans les logs
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials', // ID défini dans Jenkins
                    usernameVariable: 'DOCKER_USER',         // Variable pour le username
                    passwordVariable: 'DOCKER_PASS'          // Variable pour le mot de passe
                )]) {
                    // Connexion sécurisée à Docker Hub (--password-stdin évite le mot de passe en clair)
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"

                    // Pousser l'image avec le tag numéro de build
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"

                    // Pousser l'image avec le tag latest
                    sh "docker push ${DOCKER_IMAGE}:latest"

                    // Se déconnecter de Docker Hub
                    sh "docker logout"
                }
            }
        }
    }

    // =============================
    // ACTIONS POST-PIPELINE
    // =============================
    post {
        // Si tous les stages réussissent
        success {
            echo "✅ Pipeline réussi ! Image publiée : ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }

        // Si un stage échoue, les suivants sont ignorés
        failure {
            echo "❌ Pipeline échoué ! Vérifiez les logs."
        }

        // Toujours exécuté (succès ou échec) : nettoyage de l'image locale
        always {
            // Supprimer l'image locale pour libérer de l'espace (|| true = pas d'erreur si inexistante)
            sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
        }
    }
}