<template>
    <nav class="navbar" style="background-color: #1c1b1d; color: #b1b2b5;">
        <div class="container-fluid">
            <a class="navbar-brand d-flex align-items-center" href="/">
                <div class="rounded-circle" style="width: 40px; height: 40px; background-color: #b1b2b5; margin-right: 10px;"></div>
                <span class="navbar-brand m-0 h1" style="color: #f36c1b;">EDDAI</span>
            </a>
            <div class="d-flex justify-content-center flex-grow-1">
                <ul class="navbar-nav d-flex flex-row">
                    <li v-for="item in navItems" :key="item.name" class="nav-item mx-3">
                        <a class="nav-link" :href="item.link" style="color: #f36c1b;">{{ item.name }}</a>
                    </li>
                </ul>
            </div>
            <button class="btn login-btn" style="background-color: #f36c1b; color: #1c1b1d; ">Login</button>
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

<style>
.login-btn {
    box-shadow: inset 4px 4px 4px 0px #00000033;
}

.navbar-nav .nav-link {
    text-decoration: none;
    font-weight: bold;
}

.navbar-nav .nav-link:hover {
    color: #aac9de;
}
</style>