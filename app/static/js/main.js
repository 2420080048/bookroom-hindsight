const searchInput = document.getElementById("searchInput");
const cards = [...document.querySelectorAll(".book-card")];
const filterButtons = document.querySelectorAll(".filter-button");
const moodButtons = document.querySelectorAll(".mood-card");

let currentFilter = "All";

function filterBooks() {

    const search = searchInput
        ? searchInput.value.toLowerCase().trim()
        : "";

    let visible = 0;

    cards.forEach(card => {

        const searchData = card.dataset.search;
        const genre = card.dataset.genre;
        const author = card.dataset.author;

        const matchesSearch =
            searchData.includes(search);

        const matchesFilter =
            currentFilter === "All" ||
            genre === currentFilter ||
            author === currentFilter;

        if (matchesSearch && matchesFilter) {

            card.style.display = "";
            visible++;

        } else {

            card.style.display = "none";

        }

    });

    document.getElementById("noResults").style.display =
        visible === 0 ? "block" : "none";
}


if (searchInput) {

    searchInput.addEventListener(
        "input",
        filterBooks
    );

}


filterButtons.forEach(button => {

    button.addEventListener("click", () => {

        filterButtons.forEach(btn =>
            btn.classList.remove("active")
        );

        button.classList.add("active");

        currentFilter =
            button.dataset.filter;

        filterBooks();

    });

});


moodButtons.forEach(button => {

    button.addEventListener("click", () => {

        currentFilter =
            button.dataset.filter;

        filterButtons.forEach(btn => {

            btn.classList.toggle(
                "active",
                btn.dataset.filter === currentFilter
            );

        });

        filterBooks();

        document
            .getElementById("books")
            .scrollIntoView({
                behavior: "smooth"
            });

    });

});



/* ---------------- BOOK COVERS ---------------- */

const coverCache =
    JSON.parse(
        localStorage.getItem("bookCoverCache") || "{}"
    );


async function loadBookCover(img) {

    const title = img.dataset.title;
    let author = img.dataset.author;

    author =
        author
            .split("&")[0]
            .trim();

    const cacheKey =
        `${title}-${author}`;

    if (coverCache[cacheKey]) {

        img.src =
            coverCache[cacheKey];

        return;

    }


    try {

        const query =
            encodeURIComponent(
                `intitle:${title} inauthor:${author}`
            );

        const response =
            await fetch(
                `https://www.googleapis.com/books/v1/volumes?q=${query}&maxResults=1`
            );

        const data =
            await response.json();


        const book =
            data.items?.[0]?.volumeInfo;


        let cover =
            book?.imageLinks?.thumbnail ||
            book?.imageLinks?.smallThumbnail;


        if (cover) {

            cover =
                cover.replace(
                    "http://",
                    "https://"
                );


            coverCache[cacheKey] =
                cover;


            localStorage.setItem(
                "bookCoverCache",
                JSON.stringify(coverCache)
            );


            img.src =
                cover;

        }

    } catch (error) {

        console.log(
            "Cover unavailable:",
            title
        );

    }

}


document
    .querySelectorAll(".book-cover")
    .forEach(img => {

        img.addEventListener(
            "load",
            () =>
                img.classList.add("loaded")
        );

        img.addEventListener(
            "error",
            () =>
                img.classList.remove("loaded")
        );

        loadBookCover(img);

    });



/* ---------------- WISHLIST ---------------- */

let wishlist =
    JSON.parse(
        localStorage.getItem("wishlist") || "[]"
    );


document
    .querySelectorAll(".wishlist-heart")
    .forEach(button => {

        const title =
            button.dataset.title;


        if (wishlist.includes(title)) {

            button.classList.add("active");

            button.innerText =
                "♥";

        }


        button.addEventListener(
            "click",
            () => {

                if (
                    wishlist.includes(title)
                ) {

                    wishlist =
                        wishlist.filter(
                            item =>
                                item !== title
                        );

                    button.classList.remove(
                        "active"
                    );

                    button.innerText =
                        "♡";

                    showToast(
                        "Removed from wishlist"
                    );

                } else {

                    wishlist.push(title);

                    button.classList.add(
                        "active"
                    );

                    button.innerText =
                        "♥";

                    showToast(
                        "Saved to your wishlist ♡"
                    );

                }


                localStorage.setItem(
                    "wishlist",
                    JSON.stringify(wishlist)
                );

            }
        );

    });



/* ---------------- CART ---------------- */

let cart =
    JSON.parse(
        localStorage.getItem("cart") || "[]"
    );


const cartDrawer =
    document.getElementById(
        "cartDrawer"
    );


const drawerOverlay =
    document.getElementById(
        "drawerOverlay"
    );


const openCart =
    document.getElementById(
        "openCart"
    );


const closeCart =
    document.getElementById(
        "closeCart"
    );


function openDrawer() {

    cartDrawer.classList.add("open");

    drawerOverlay.classList.add("open");

}


function closeDrawer() {

    cartDrawer.classList.remove("open");

    drawerOverlay.classList.remove("open");

}


openCart.addEventListener(
    "click",
    openDrawer
);


closeCart.addEventListener(
    "click",
    closeDrawer
);


drawerOverlay.addEventListener(
    "click",
    closeDrawer
);



function saveCart() {

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

    renderCart();

}



function addToCart(
    title,
    author,
    price
) {

    const exists =
        cart.some(
            item =>
                item.title === title
        );


    if (exists) {

        showToast(
            "That book is already in your bag ♡"
        );

        openDrawer();

        return;

    }


    cart.push({
        title,
        author,
        price: Number(price)
    });


    saveCart();

    showToast(
        `${title} added to your bag`
    );

}



document
    .querySelectorAll(".quick-add")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                addToCart(
                    button.dataset.title,
                    button.dataset.author,
                    button.dataset.price
                );

            }
        );

    });



document
    .querySelectorAll(".series-add")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                addToCart(
                    button.dataset.title,
                    `${button.dataset.author} • Complete Series`,
                    button.dataset.price
                );

            }
        );

    });



function removeItem(index) {

    cart.splice(
        index,
        1
    );

    saveCart();

}



function renderCart() {

    const container =
        document.getElementById(
            "cartItems"
        );


    const empty =
        document.getElementById(
            "emptyCart"
        );


    const count =
        document.getElementById(
            "cartCount"
        );


    const total =
        document.getElementById(
            "cartTotal"
        );


    count.textContent =
        cart.length;


    if (cart.length === 0) {

        container.innerHTML = "";

        empty.style.display =
            "block";

        total.textContent =
            "₹0";

        return;

    }


    empty.style.display =
        "none";


    container.innerHTML =
        cart
            .map(
                (item, index) => `

                <div class="cart-item">

                    <div class="cart-item-cover">
                        ${item.title}
                    </div>

                    <div>

                        <h4>
                            ${item.title}
                        </h4>

                        <p>
                            ${item.author}
                        </p>

                        <button
                            class="remove-item"
                            onclick="removeItem(${index})"
                        >
                            Remove
                        </button>

                    </div>

                    <strong>
                        ₹${item.price}
                    </strong>

                </div>

            `
            )
            .join("");


    const totalValue =
        cart.reduce(
            (sum, item) =>
                sum + item.price,
            0
        );


    total.textContent =
        `₹${totalValue}`;

}



window.removeItem =
    removeItem;



/* ---------------- TOAST ---------------- */

let toastTimer;


function showToast(message) {

    const toast =
        document.getElementById(
            "toast"
        );


    toast.textContent =
        message;


    toast.classList.add(
        "show"
    );


    clearTimeout(
        toastTimer
    );


    toastTimer =
        setTimeout(
            () =>
                toast.classList.remove(
                    "show"
                ),
            2200
        );

}


renderCart();
/* ---------------- CHECKOUT ---------------- */

const checkoutButton =
    document.querySelector(
        ".checkout-button"
    );


if (checkoutButton) {

    checkoutButton.addEventListener(
        "click",
        () => {

            if (cart.length === 0) {

                showToast(
                    "Your bag is empty ♡"
                );

                return;
            }

            window.location.href =
                "/checkout";

        }
    );

}

