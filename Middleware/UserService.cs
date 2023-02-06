using Datalayer;
using Datalayer.Models;
using LanguageExt.Common;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Middleware
{
    public class UserService : IUserService
    {
        private AggDbContext _dbContext;
        private IPasswordHasher<User> _passwordHasher;
        IDataProtectionProvider _provider;
        public UserService(AggDbContext dbContext, IPasswordHasher<User> passwordHasher, IDataProtectionProvider provider) 
        {
            _dbContext= dbContext;
            _passwordHasher= passwordHasher;
            _provider=provider;
        }
        public string StartResetPassword(string email)
        {
            var protector = _provider.CreateProtector("PasswordReset");
            var user = GetUser(email);
            return protector.Protect(user.Email);
        }

        public bool EndPasswordReset(string hash, string email, string newPassword) 
        {
            var protector = _provider.CreateProtector("PasswordReset");
            var hashEmail = protector.Unprotect(hash);
            if(hashEmail != email)
            {
                return false;
            }

            var user = GetUser(email);
            user.PasswordHash = _passwordHasher.HashPassword(user, newPassword);
            _dbContext.SaveChanges();

            return true;
        }
        public User GetUser(string email) 
        {
            return _dbContext.Users.First(u => u.Email.Equals(email));
        }

        public User Login(string email, string password)
        {
            var user = GetUser(email);

            var result = _passwordHasher.VerifyHashedPassword(user, user.PasswordHash, password);

            if(result == PasswordVerificationResult.Failed)
            {
                return default;
            }
            return user;

        }

        public async Task<User> RegisterUser(string username, string password, string email)
        {
            var userExists = await _dbContext.Users.AnyAsync(u=>u.Email.Equals(email));

            if (userExists) 
            {
                return default;
            }

            var user = new User()
            {
                Email = email,
                Name = username,
                UserId = Guid.NewGuid()
            };

            var passwordHash = _passwordHasher.HashPassword(user,password);

            user.PasswordHash= passwordHash;

            _dbContext.Users.Add(user);

            _dbContext.SaveChanges();
            return user;
        }
    }
}
