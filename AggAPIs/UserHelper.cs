using Datalayer.Models;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace AggAPIs
{
    public class UserHelper
    {
        public static ClaimsPrincipal Convert(User user)
        {
            var claims = new List<Claim>()
            {
                new Claim("userid", user.UserId.ToString()),
                new Claim("useremail", user.Email)
            };

            claims.AddRange(user.Claims.Select(x => new Claim(x.Type, x.Value)));

            var identity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);
            return new ClaimsPrincipal(identity);
        }
    }
}
