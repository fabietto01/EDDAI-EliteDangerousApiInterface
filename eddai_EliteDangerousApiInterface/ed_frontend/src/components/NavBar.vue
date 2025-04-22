<template>
    <nav class="navbar navbar-expand-md">
        <div class="container-fluid">
            <a class="navbar-brand d-flex align-items-center" href="/">
                <div class="rounded-circle" style="width: 40px; height: 40px; background-color: #b1b2b5; margin-right: 10px;"></div>
                <span class="navbar-brand m-0 h1" style="color: #f36c1b;">EDDAI</span>
            </a>
            <button class="navbar-toggler nav-btn" 
                type="button" data-bs-toggle="collapse" 
                data-bs-target="#FullScreenNav" 
                aria-controls="FullScreenNav" 
                aria-expanded="false" 
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="FullScreenNav">
                
                <ul class="navbar-nav navbar-text mx-auto justify-content-center">
                    <li v-for="item in navItems" :key="item.name" class="nav-item">
                        <a class="nav-link" :href="item.link">{{ item.name }}</a>
                    </li>
                </ul>
            </div>
            <button class="btn nav-btn d-none d-md-block">Login</button>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'NavBar',
    data() {
        return {
            navItems: [
                { name: 'System', link: '/systems/' },
                { name: 'Station', link: '#' },
                { name: 'Body', link: '#' },
            ],
        };
    },
};
</script>

<style >
.navbar{
    background-color: #1c1b1d; 
}

.nav-btn {
    background-color: #f36c1b; color: #1c1b1d;
    box-shadow: inset 4px 4px 4px 0px #00000033;
}

.navbar-nav .nav-link {
    color: #f36c1b;
    text-decoration: none;
    font-weight: bold;
}

.navbar-nav .nav-link:hover {
    color: #aac9de;
}

@media screen and (max-width: 768px) {
    .navbar-collapse {
        display: flex;
        align-items: center;
        justify-content: center;

        text-align: center;
        height: 1000px;
    } 
    .navbar-nav .nav-link {
        font-size: 40px;
    }
    
}


</style>