"""
End-to-End tests using Playwright
Simulates real user interactions with the FastAPI Calculator
"""
import pytest
from playwright.sync_api import sync_playwright, expect
import time
import subprocess
import signal
import os


@pytest.fixture(scope="module")
def server():
    """Start the FastAPI server for E2E tests"""
    # Start the server as a background process
    env = os.environ.copy()
    server_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    
    # Wait for server to start
    time.sleep(3)
    
    yield server_process
    
    # Cleanup: stop the server
    server_process.send_signal(signal.SIGTERM)
    server_process.wait(timeout=5)


@pytest.fixture(scope="function")
def browser_context():
    """Create a browser context for each test"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


class TestSwaggerUIInteraction:
    """Test user interactions with Swagger UI"""
    
    def test_swagger_ui_loads(self, server, browser_context):
        """Test that Swagger UI page loads successfully"""
        page = browser_context.new_page()
        page.goto("http://localhost:8000/docs")
        
        # Wait for Swagger UI to load
        page.wait_for_selector(".swagger-ui", timeout=10000)
        
        # Check title
        assert "FastAPI" in page.title()
        
        # Check that API title is visible
        expect(page.locator("text=FastAPI Calculator")).to_be_visible()
        
    def test_swagger_ui_displays_endpoints(self, server, browser_context):
        """Test that all endpoints are visible in Swagger UI"""
        page = browser_context.new_page()
        page.goto("http://localhost:8000/docs")
        
        page.wait_for_selector(".swagger-ui", timeout=10000)
        
        # Check for main endpoints
        expect(page.locator("text=/calculate")).to_be_visible()
        expect(page.locator("text=/health")).to_be_visible()
        
    def test_calculate_endpoint_expansion(self, server, browser_context):
        """Test expanding the calculate endpoint in Swagger UI"""
        page = browser_context.new_page()
        page.goto("http://localhost:8000/docs")
        
        page.wait_for_selector(".swagger-ui", timeout=10000)
        
        # Find and click the /calculate endpoint
        calculate_endpoint = page.locator(".opblock-post").filter(has_text="/calculate")
        calculate_endpoint.click()
        
        # Wait for expansion
        time.sleep(1)
        
        # Check if "Try it out" button is visible
        expect(page.locator("button:has-text('Try it out')").first).to_be_visible()


class TestAPICalculations:
    """Test actual calculations through API calls"""
    
    def test_addition_via_api(self, server, browser_context):
        """Test addition calculation via direct API call"""
        page = browser_context.new_page()
        
        # Make API request using fetch
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: 10, num2: 5, operation: 'add'})
                });
                return await response.json();
            }
        """)
        
        assert result["result"] == 15.0
        assert result["operation"] == "add"
        
    def test_subtraction_via_api(self, server, browser_context):
        """Test subtraction calculation via direct API call"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: 20, num2: 8, operation: 'subtract'})
                });
                return await response.json();
            }
        """)
        
        assert result["result"] == 12.0
        assert result["operation"] == "subtract"
        
    def test_multiplication_via_api(self, server, browser_context):
        """Test multiplication calculation via direct API call"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: 6, num2: 7, operation: 'multiply'})
                });
                return await response.json();
            }
        """)
        
        assert result["result"] == 42.0
        assert result["operation"] == "multiply"
        
    def test_division_via_api(self, server, browser_context):
        """Test division calculation via direct API call"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: 20, num2: 4, operation: 'divide'})
                });
                return await response.json();
            }
        """)
        
        assert result["result"] == 5.0
        assert result["operation"] == "divide"
        
    def test_division_by_zero_error(self, server, browser_context):
        """Test division by zero error handling"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: 10, num2: 0, operation: 'divide'})
                });
                return {
                    status: response.status,
                    data: await response.json()
                };
            }
        """)
        
        assert result["status"] == 400
        assert "Cannot divide by zero" in result["data"]["detail"]
        
    def test_invalid_operation_error(self, server, browser_context):
        """Test invalid operation error handling"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: 10, num2: 5, operation: 'power'})
                });
                return {
                    status: response.status,
                    data: await response.json()
                };
            }
        """)
        
        assert result["status"] == 400
        assert "Invalid operation" in result["data"]["detail"]


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self, server, browser_context):
        """Test health check endpoint returns healthy status"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/health');
                return await response.json();
            }
        """)
        
        assert result["status"] == "healthy"


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self, server, browser_context):
        """Test root endpoint returns welcome message"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/');
                return await response.json();
            }
        """)
        
        assert "Welcome to FastAPI Calculator" in result["message"]
        assert "endpoints" in result


class TestMultipleOperations:
    """Test performing multiple operations in sequence"""
    
    def test_sequential_operations(self, server, browser_context):
        """Test performing multiple calculations in sequence"""
        page = browser_context.new_page()
        
        # Perform multiple operations
        operations = [
            {"num1": 10, "num2": 5, "operation": "add", "expected": 15},
            {"num1": 20, "num2": 4, "operation": "subtract", "expected": 16},
            {"num1": 6, "num2": 7, "operation": "multiply", "expected": 42},
            {"num1": 100, "num2": 5, "operation": "divide", "expected": 20},
        ]
        
        for op in operations:
            result = page.evaluate(f"""
                async () => {{
                    const response = await fetch('http://localhost:8000/calculate', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            num1: {op['num1']}, 
                            num2: {op['num2']}, 
                            operation: '{op['operation']}'
                        }})
                    }});
                    return await response.json();
                }}
            """)
            
            assert result["result"] == op["expected"]
            assert result["operation"] == op["operation"]


class TestConcurrentRequests:
    """Test handling concurrent requests"""
    
    def test_concurrent_calculations(self, server, browser_context):
        """Test multiple concurrent calculations"""
        page = browser_context.new_page()
        
        # Make multiple concurrent requests
        result = page.evaluate("""
            async () => {
                const requests = [
                    fetch('http://localhost:8000/calculate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({num1: 10, num2: 5, operation: 'add'})
                    }),
                    fetch('http://localhost:8000/calculate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({num1: 20, num2: 4, operation: 'multiply'})
                    }),
                    fetch('http://localhost:8000/calculate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({num1: 100, num2: 10, operation: 'divide'})
                    })
                ];
                
                const responses = await Promise.all(requests);
                const results = await Promise.all(responses.map(r => r.json()));
                return results;
            }
        """)
        
        assert len(result) == 3
        assert result[0]["result"] == 15.0
        assert result[1]["result"] == 80.0
        assert result[2]["result"] == 10.0


class TestEdgeCasesE2E:
    """Test edge cases through E2E tests"""
    
    def test_large_numbers(self, server, browser_context):
        """Test calculations with large numbers"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: 999999999, num2: 1, operation: 'add'})
                });
                return await response.json();
            }
        """)
        
        assert result["result"] == 1000000000.0
        
    def test_decimal_precision(self, server, browser_context):
        """Test calculations with decimal numbers"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: 0.1, num2: 0.2, operation: 'add'})
                });
                return await response.json();
            }
        """)
        
        assert abs(result["result"] - 0.3) < 1e-10
        
    def test_negative_numbers(self, server, browser_context):
        """Test calculations with negative numbers"""
        page = browser_context.new_page()
        
        result = page.evaluate("""
            async () => {
                const response = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: -10, num2: -5, operation: 'multiply'})
                });
                return await response.json();
            }
        """)
        
        assert result["result"] == 50.0
