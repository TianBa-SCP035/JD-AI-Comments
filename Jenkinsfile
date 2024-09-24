import groovy.transform.Field

@Field def job_name=""

node()
{
    // 获取当前job名称。也可以按需自定义
    job_name="${env.JOB_NAME}".replace('%2F', '/').split('/')
    job_name=job_name[0]


    ws("$workspace")
    {
        dir("pipeline")
        {   
            // clone Jenkinsfile项目
            git credentialsId: 'git-cicd', branch: 'release/1.0', url: 'http://gitlab-tech.ikunchi.com/ops/kc-cicd.git'

            // 根据job name、构建分支，自动加载对应的Jenkinsfile
            def check_groovy_file="${workspace}/pipeline/aicomposer/ci/image/Jenkinsfile"
            //println workspace
            load "${check_groovy_file}"
        }
    }
}
