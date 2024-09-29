from flask import Flask, render_template, request

app = Flask(__name__)  # Defaults to looking for templates in the 'templates' directory

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    eps_surprise = eps_yoy = revenue_surprise = revenue_yoy = None
    unit = 'millions'
    unit_display = 'M'
    estimated_eps = actual_eps = prev_eps = estimated_revenue = actual_revenue = prev_revenue = ""
    actual_eps_display = estimated_eps_display = prev_eps_display = ""

    if request.method == 'POST':
        try:
            unit = 'millions' if 'unit' in request.form else 'thousands'
            unit_display = 'M' if unit == 'millions' else 'K'
            estimated_eps = request.form['estimated_eps']
            actual_eps = request.form['actual_eps']
            prev_eps = request.form['prev_eps']
            estimated_revenue = request.form['estimated_revenue']
            actual_revenue = request.form['actual_revenue']
            prev_revenue = request.form['prev_revenue']

            estimated_eps_float = float(estimated_eps)
            actual_eps_float = float(actual_eps)
            prev_eps_float = float(prev_eps)
            estimated_revenue_float = float(estimated_revenue)
            actual_revenue_float = float(actual_revenue)
            prev_revenue_float = float(prev_revenue)

            # Calculate EPS Surprise
            if estimated_eps_float != 0:
                eps_surprise_val = ((actual_eps_float - estimated_eps_float) / abs(estimated_eps_float)) * 100
                eps_surprise = f"{'+' if eps_surprise_val > 0 else ''}{eps_surprise_val:.0f}%"  # Zero decimals
            else:
                eps_surprise = "N/A (Estimated EPS is zero)"
            
            # Calculate EPS % YoY
            if prev_eps_float != 0:
                eps_yoy_val = ((actual_eps_float - prev_eps_float) / abs(prev_eps_float)) * 100
                eps_yoy = f"{'+' if eps_yoy_val > 0 else ''}{eps_yoy_val:.0f}%"  # Zero decimals
            else:
                eps_yoy = "N/A (Previous EPS is zero)"
            
            # Calculate Revenue Surprise
            if estimated_revenue_float != 0:
                revenue_surprise_val = ((actual_revenue_float - estimated_revenue_float) / abs(estimated_revenue_float)) * 100
                revenue_surprise = f"{'+' if revenue_surprise_val > 0 else ''}{revenue_surprise_val:.0f}%"  # Zero decimals
            else:
                revenue_surprise = "N/A (Estimated Revenue is zero)"
            
            # Calculate Revenue % YoY
            if prev_revenue_float != 0:
                revenue_yoy_val = ((actual_revenue_float - prev_revenue_float) / abs(prev_revenue_float)) * 100
                revenue_yoy = f"{'+' if revenue_yoy_val > 0 else ''}{revenue_yoy_val:.0f}%"  # Zero decimals
            else:
                revenue_yoy = "N/A (Previous Revenue is zero)"
            
            # Convert EPS values to cents if they are between -0.99 and 0.99
            actual_eps_display = f"{actual_eps_float * 100:.0f}c" if -0.99 < actual_eps_float < 0.99 else f"{actual_eps_float:.2f}"
            estimated_eps_display = f"{estimated_eps_float * 100:.0f}c" if -0.99 < estimated_eps_float < 0.99 else f"{estimated_eps_float:.2f}"
            prev_eps_display = f"{prev_eps_float * 100:.0f}c" if -0.99 < prev_eps_float < 0.99 else f"{prev_eps_float:.2f}"

        except ValueError:
            error = "Invalid input. Please enter valid numbers."

    return render_template(
        'index.html', 
        eps_surprise=eps_surprise, 
        eps_yoy=eps_yoy, 
        revenue_surprise=revenue_surprise, 
        revenue_yoy=revenue_yoy,
        unit=unit,
        unit_display=unit_display,
        estimated_eps=estimated_eps,
        actual_eps=actual_eps,
        prev_eps=prev_eps,
        estimated_revenue=estimated_revenue,
        actual_revenue=actual_revenue,
        prev_revenue=prev_revenue,
        error=error,
        actual_eps_display=actual_eps_display,
        estimated_eps_display=estimated_eps_display,
        prev_eps_display=prev_eps_display
    )

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
