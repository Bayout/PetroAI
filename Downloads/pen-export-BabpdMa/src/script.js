 document.getElementById("sendWhatsapp").addEventListener("click", function() {
        const phoneNumber = "+5522999225626"; // Seu número de telefone
        const message = encodeURIComponent(document.getElementById("message").value);

        if (message) {
            const whatsappURL = `https://wa.me/${phoneNumber}?text=${message}`;
            window.location.href = whatsappURL;
            
            // Ocultar o formulário
            document.getElementById("contactForm").style.display = "none";
        } else {
            alert("Por favor, preencha a mensagem.");
        }
    });