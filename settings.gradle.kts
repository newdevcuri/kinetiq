pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "Kinetiq"

include(":app")
include(":core:designsystem")
include(":core:database")
include(":core:model")
include(":core:data")
include(":core:engine")
include(":core:healthconnect")
include(":feature:onboarding")
include(":feature:dashboard")
include(":feature:train")
include(":feature:workout")
include(":feature:library")
include(":feature:progress")
