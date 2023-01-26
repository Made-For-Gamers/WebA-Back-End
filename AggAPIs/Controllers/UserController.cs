using AggAPIs.Models;
using Datalayer.Models;
using LanguageExt.Pipes;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Middleware;

namespace AggAPIs.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        private IUserService _userService;
        private HttpContext _ctx;
        public UserController(IUserService userService, IHttpContextAccessor ctx)
        {
            _userService = userService;
            _ctx = ctx.HttpContext;
        }

        [HttpPost("/login")]
        [AllowAnonymous]
        public async Task<IActionResult> Login([FromBody] LoginModel loginData)
        {
            var user = _userService.Login(loginData.Email, loginData.Password);
            if (user != default)
            {
                await _ctx.SignInAsync(
                    CookieAuthenticationDefaults.AuthenticationScheme,
                    UserHelper.Convert(user)
                    );
                return Ok();
            }
            else
            {
                return BadRequest();
            }

        }

        [HttpPost("/register")]
        [AllowAnonymous]
        public async Task<IActionResult> Register([FromBody] RegisterModel registerData)
        {
            var user = await _userService.RegisterUser(
                registerData.UserName,
                registerData.Password,
                registerData.Email);

            if (user != default)
            {
                await _ctx.SignInAsync(
                    CookieAuthenticationDefaults.AuthenticationScheme,
                    UserHelper.Convert(user)
                    );
                return Ok();
            }
            return BadRequest();
        }

        [HttpGet("/startPasswordReset")]
        [Authorize]
        public async Task<IActionResult> StartPasswordReset(string email)
        {
            var hash = _userService.StartResetPassword(email);

            //TODO: Think of the bad case scenario
            return Ok(hash);
        }

        [HttpPost("/endPasswordReset")]
        [Authorize]
        public async Task<IActionResult> EndPasswordReset([FromBody] PasswordResetModel passResetData)
        {
            var reset = _userService.EndPasswordReset(
                passResetData.Hash, 
                passResetData.Email, 
                passResetData.NewPassword);

            if (reset) { return Ok(); }
            return BadRequest();
        }
    }
}
