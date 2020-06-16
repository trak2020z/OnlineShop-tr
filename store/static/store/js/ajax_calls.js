function add_one(product_id, amount)
{
    $.ajax({
        'url': '/add_one/',
        'data': {
            'item': product_id,
            'amount': amount
        },
        'dataType': 'json',
        'success': function(data){
            if(data.modified){
                alert("Product added to cart.")
            }
        }
    });
}

function set_amount(product_id, amount)
{
    $.ajax({
        'url': '/set_amount/',
        'data': {
            'item': product_id,
            'amount': amount
        },
        'dataType': 'json',
        'success': function(data){
            if(data.deleted){
                alert('Product removed from cart');
                top.location.reload();
            }
            else if (data.price == -1){
                alert('Wrong data!')
            }
            else{
                if(data.msg){
                    alert(data.msg);
                    amount = 100;
                    $("#amount_"+product_id).val(amount);
                }

                $("#price_"+product_id).html(
                    (amount * data.price).toFixed(2));
                
                var prices = $(".product-price");
                var total = 0;
                for(p of prices){
                    total = total + parseFloat(p.innerHTML);
                }

                $("#total-price").html(total.toFixed(2));
            }
        }
    });
}


function remove_from_cart(product_id){
    $.ajax({
        'url': '/remove_all/',
        'data': {
            'item': product_id
        },
        'dataType': 'json',
        'success': function(data){
            if(data.modified){
                top.location.reload();
            }
        }
    });
}